import redis
import json
from datetime import datetime

class InMemoryCRUD():
    in_memory = redis.Redis(host='redis', port=6379, decode_responses=True)

    def store_code_data_in_memory(self, program_id, file_name, code, code_info_serialized, frama_results):
        key_program_metadata = f"program:{program_id}:metadata"
        key_program_invariants = f"program:{program_id}:invariants"

        valid = invalid = total = 0

        for result in frama_results:
            if result["validated"] is True:
                valid += 1
            elif result["validated"] is False:
                invalid += 1

            total += 1

        metadata_data = {
            "FILE_REFERENCE": file_name,
            "UUID": str(program_id),
            "SOURCE_CODE": code,
            "AST_INFORMATION": json.dumps(code_info_serialized),
            "TOTAL_INVARIANTS": total,
            "VALID_COUNT": valid,
            "INVALID_COUNT": invalid
        }

        self.in_memory.hmset(key_program_metadata, metadata_data)

        for result in frama_results:
            inv_data = {
                "INVARIANT": result["invariant"],
                "VALID": str(result["validated"]),
            }

            self.in_memory.rpush(key_program_invariants, json.dumps(inv_data))

    def get_code_data_in_memory(self, program_id, loop_id):
        key = f"loop:{program_id}:{loop_id}"
        data = self.in_memory.hgetall(key)

        data["variable_roles"] = json.loads(data["variable_roles"])
        data["bounds"] = json.loads(data["bounds"])
        data["invariants"] = json.loads(data["invariants"])
        return data

    def fetch_all_keys(self):
        cursor = 0
        all_keys = []

        while True:
            cursor, partial_keys = self.in_memory.scan(cursor=cursor, match="program:*:metadata")
            all_keys.extend(partial_keys)

            if cursor == 0:
                break

        return all_keys

    def is_file_processed(self, file_name):
        try:
            keys = self.fetch_all_keys()

            if len(keys) == 0 :
                return

            for key in keys:
                if file_name == self.in_memory.hget(key, 'FILE_REFERENCE') :
                    return True
        except Exception as ex :
            print(ex)
            pass
