import subprocess


class EC2:
    def __init__(self, *args, **kwargs):
        self.attrib = kwargs["attrib"]
        self.limit = kwargs["limit"]
        self.output = kwargs["output"]
        self.tag_key = kwargs["tag_key"]
        self.tag_value = kwargs["tag_value"]

    def run(self):
        cmd = [
            "aws",
            "ec2",
            "describe-instances",
            "--output",
            self.output,
            "--filter",
            f"Name=tag:{self.tag_key},Values={self.tag_value}",
            "--query",
            f"Reservations[*].Instances[*].[{','.join(self.attrib)}]",
        ]

        res = subprocess.run(cmd, capture_output=True, encoding="utf-8")

        if res.returncode != 0:
            raise Exception(res.stderr)

        # No error, thus we print lines.
        if self.limit == 0:
            print(res.stdout)
        else:
            n = 0
            for line in res.stdout.split("\n"):
                print(line)
                n += 1
                if n >= self.limit:
                    break
