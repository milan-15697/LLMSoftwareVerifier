import json, io
import re
from pycparser import c_ast
from difflib import SequenceMatcher
import redis
import textwrap
from InMemoryCRUD import InMemoryCRUD

class CodeComparator(c_ast.NodeVisitor):
    in_memory_obj = InMemoryCRUD()

    def normalize_ast(self, ast_data):
        def normalize_value(value, key):
            if isinstance(value, str) and key in ["cond", "body"]:
                value = re.sub(r'ID: (\w+)', 'ID: VAR_LOOP', value)
                value = re.sub(r'Constant: (int|float), (\d+(\.\d+)?)', 'Constant: \\1, NUM_VALUE', value)
            return value

        def recursive_normalize(data):
            if isinstance(data, list):
                return [recursive_normalize(item) for item in data]
            elif isinstance(data, dict):
                return {key: recursive_normalize(normalize_value(value, key)) for key, value in data.items()}
            else:
                return data

        return recursive_normalize(ast_data)

    def calculate_similarity(self, codeA_AST, codeB_AST):
        try:
            codeA_AST = json.dumps(self.normalize_ast(json.loads(codeA_AST)))
            codeB_AST = json.dumps(self.normalize_ast(json.loads(codeB_AST)))
            # print("Normalized AST 1: ", codeA_AST, "\n", "Normalized AST 2: ", codeB_AST)
            return SequenceMatcher(None, codeA_AST, codeB_AST).ratio()
        except Exception as ex:
            print("Exception in normalizing the AST and similarity score calc", ex)

    def similarity_lookup_and_compare(self, code_under_check_serialized, file_name):
        keys = self.in_memory_obj.fetch_all_keys()
        if len(keys) == 0:
            return

        programs_in_memory = [self.in_memory_obj.in_memory.hgetall(key) for key in keys]
        similarities = []

        for program in programs_in_memory:
            stored_ast = program['AST_INFORMATION']
            if program['FILE_REFERENCE'] == file_name or stored_ast == None:
                continue
            score = self.calculate_similarity(json.dumps(code_under_check_serialized), stored_ast)
            # print("Score", score)
            similarities.append((program['UUID'],program['FILE_REFERENCE'] , score))

        similarity_score = max(similarities, key=lambda x: x[2])
        print("Max Similarity", similarity_score)

        if similarity_score[2] < 0.8 :
            print("No similar program found in memory")
            return None

        k_md = "program:"+ max(similarities, key=lambda x: x[2])[0] + ":metadata"
        k_inv = "program:"+ max(similarities, key=lambda x: x[2])[0] + ":invariants"

        invariants = self.in_memory_obj.in_memory.lrange(k_inv, 0, -1)
        metadata = self.in_memory_obj.in_memory.hgetall(k_md)
        return (max(similarities, key=lambda x: x[2]), invariants, metadata)
