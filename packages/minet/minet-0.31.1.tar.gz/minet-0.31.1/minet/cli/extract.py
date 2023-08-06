# =============================================================================
# Minet Extract Content CLI Action
# =============================================================================
#
# Logic of the extract action.
#
import csv
import gzip
import codecs
import warnings
from multiprocessing import Pool
from tqdm import tqdm
from dragnet import extract_content

from minet.encodings import is_supported_encoding
from minet.cli.utils import (
    custom_reader,
    open_output_file,
    create_report_iterator
)
from minet.cli.reporters import report_error

from minet.exceptions import UnknownEncodingError

OUTPUT_ADDITIONAL_HEADERS = ['extract_error', 'extracted_text']


def worker(payload):
    line, _, path, encoding, content, _ = payload

    if not is_supported_encoding(encoding):
        return UnknownEncodingError('Unknown encoding: "%s"' % encoding), line, None

    # Reading file
    if content is None:
        try:
            if path.endswith('.gz'):
                with open(path, 'rb') as f:
                    raw_html_bytes = gzip.decompress(f.read())

                raw_html = raw_html_bytes.decode(encoding, errors='replace')
            else:
                with codecs.open(path, 'r', encoding=encoding, errors='replace') as f:
                    raw_html = f.read()
        except UnicodeDecodeError as e:
            return e, line, None
    else:
        raw_html = content

    # Attempting extraction
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            content = extract_content(raw_html)
    except BaseException as e:
        return e, line, None

    return None, line, content


def extract_action(namespace):
    input_headers, pos, reader = custom_reader(namespace.report, ('status', 'filename', 'encoding'))

    selected_fields = namespace.select.split(',') if namespace.select else None
    selected_pos = [input_headers.index(h) for h in selected_fields] if selected_fields else None

    output_headers = (list(input_headers) if not selected_pos else [input_headers[i] for i in selected_pos])
    output_headers += OUTPUT_ADDITIONAL_HEADERS

    output_file = open_output_file(namespace.output)

    output_writer = csv.writer(output_file)
    output_writer.writerow(output_headers)

    loading_bar = tqdm(
        desc='Extracting content',
        total=namespace.total,
        dynamic_ncols=True,
        unit=' docs'
    )

    namespace.report.close()
    namespace.report = open(namespace.report.name)
    files = create_report_iterator(namespace, loading_bar=loading_bar)

    with Pool(namespace.processes) as pool:
        for error, line, content in pool.imap_unordered(worker, files):
            loading_bar.update()

            if error is not None:
                message = report_error(error)
                line.extend([message, ''])
                output_writer.writerow(line)
                continue

            line.extend(['', content])
            output_writer.writerow(line)

    output_file.close()
