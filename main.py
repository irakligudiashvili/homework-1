# import re

# re_pattern = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"

class Version:
    semantic_hierarchy = {
        "alpha": 1,
        "a": 1,
        "beta": 2,
        "b": 2,
        "rc": 3
    }

    def __init__(self, version):
        # match = re.match(re_pattern, version)

        # if not match:
        #     raise ValueError(f'invalid syntax: {version}')

        self.version = version
        self.parts = self.parse(version)
        # print(self.parts)

    def parse(self, version):
        parts = []

        # replace a & b
        if version[-2].isdigit() and not version[-1].isdigit():
            match version[-1]:
                case 'a':
                    version = version[:-1] + '-alpha'
                case 'b':
                    version = version[:-1] + '-beta'
                case default:
                    raise ValueError(f'invalid syntax: {version}')

        # split if prerelease
        if '-' in version:
            core, prerelease = version.split('-', 1)
        else:
            core = version
            prerelease = None

        for part in core.split('.'):
            parts.append(int(part))

        if prerelease:
            for key in prerelease.split('.'):
                if key.isdigit():
                    parts.append(int(key))
                elif key in self.semantic_hierarchy:
                    parts.append(self.semantic_hierarchy[key])
        else:
            # add magic number to make full release greater than prerelease
            parts.append(99)

        return parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __gt__(self, other):
        return self.parts > other.parts

    def __ne__(self, other):
        return self.parts != other.parts

def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.5.0", "0.25.4"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.0-rc.1", "1.0.0"),
        ("2.1.4", "2.1.4"),
        ("1.2.2", "1.2.2-alpha.1")
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), f"lt failed {left} > {right}"
        assert Version(right) > Version(left), f"gt failed {right} < {left}"
        assert Version(right) != Version(left), f"neq failed {right} == {left}"


if __name__ == "__main__":
    main()