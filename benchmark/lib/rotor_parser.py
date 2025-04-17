from lib.model_data import RotorModelData
import re

#TODO
class BTOR2RotorParser:
    pass

class SMT2RotorParser:
    HEADER_PATTERNS = {
        'source_file': re.compile(r'; for RISC-V executable obtained from (.+)'),
        'kmin': re.compile(r'; with -kmin (\d+)'),
        'kmax': re.compile(r'; with .* -kmax (\d+)'),
        'bytecode': re.compile(r'; with (\d+) bytes of code'),
        'data': re.compile(r'; and (\d+) bytes of data'),
        'virtual_address': re.compile(r'; with -virtualaddressspace (\d+)'),
        'code_word': re.compile(r'; with -codewordsize (\d+)'),
        'memory_word': re.compile(r'; with -memorywordsize (\d+)'),
        'heap': re.compile(r'; with -heapallowance (\d+)'),
        'stack': re.compile(r'; with -stackallowance (\d+)'),
        'cores': re.compile(r'; with -cores (\d+)'),
        'bytes_to_read': re.compile(r'; with -bytestoread (\d+)'),
        'nocomments': re.compile(r'; with -nocomments')
    }

    @classmethod
    def parse_header(cls, file_path):
        header = RotorModelData()
        flags = []
            
        comment_pattern = re.compile(r'^\s*;')
        blank_pattern = re.compile(r'^\s*$')
        
        with open(file_path, 'r') as f:
            for line in f:
                # Check each pattern
                for field, pattern in cls.HEADER_PATTERNS.items():
                    if match := pattern.search(line):
                        value = match.group(1) if match.groups() else None
                        cls._set_header_field(header, field, value, flags)

                # Stop when parser is out of header
                if not comment_pattern.search(line) and not blank_pattern.search(line):
                    break
        header.flags = flags
        return header

    @staticmethod
    def _set_header_field(header, field, value, flags):
        if field == 'source_file':
            header.source_file = value
        elif field == 'kmin':
            header.kmin = int(value)
        elif field == 'kmax':
            header.kmax = int(value)
        elif field == 'bytecode':
            header.bytecode_size = int(value)
        elif field == 'data':
            header.data_size = int(value)
        elif field == 'virtual_address':
            header.virtual_address_space = int(value)
        elif field == 'code_word':
            header.code_word_size = int(value)
        elif field == 'memory_word':
            header.memory_word_size = int(value)
        elif field == 'heap':
            header.heap_allowance = int(value)
        elif field == 'stack':
            header.stack_allowance = int(value)
        elif field == 'cores':
            header.cores = int(value)
        elif field == 'bytes_to_read':
            header.bytestoread = int(value)
        elif field == 'constants':
            header.constants_propagated = True
        elif field == 'nocomments':
            header.comments_removed = True
        else:
            flags.append(field.replace('_', '-'))