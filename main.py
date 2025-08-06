from functools import total_ordering


@total_ordering
class Version:
    semantic_hierarchy = {
        "alpha": 1,
        "beta": 2,
        "rc": 3
    }

    def __init__(self, version):
        self.version = version
        self.parts = self.parse(version)

    def parse(self, version):
        core = []
        prerelease = []

        if '+' in version:
            version = version.split('+')[0]

        for suffix in ['a', 'b', 'rc']:
            index = version.find(suffix)
            if index > 0 and version[index - 1].isdigit():
                match suffix:
                    case 'a':
                        replace_str = 'alpha'
                    case 'b':
                        replace_str = 'beta'
                    case 'rc':
                        replace_str = 'rc'

                core_part = version[:index]
                remaining = version[index + len(suffix):]

                if remaining:
                    version = f"{core_part}-{replace_str}.{remaining}"
                else:
                    version = f"{core_part}-{replace_str}"
                break

        if '-' in version:
            core_str, prerelease_str = version.split('-', 1)
        else:
            core_str = version
            prerelease_str = None

        for part in core_str.split('.'):
            core.append(int(part))

        if prerelease_str:
            for key in prerelease_str.split('.'):
                if key.isdigit():
                    prerelease.append(int(key))
                elif key in self.semantic_hierarchy:
                    prerelease.append(self.semantic_hierarchy[key])

        parts = [core, prerelease]
        return parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        self_core, self_pre = self.parts
        other_core, other_pre = other.parts

        if self_core != other_core:
            return self_core < other_core

        if not self_pre and other_pre:
            return False
        if self_pre and not other_pre:
            return True
        return self_pre < other_pre


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("0.25.4", "1.5.0"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.0-rc.1", "1.0.0"),
        ("2.1.4", "2.1.4"),
        ("1.2.2-alpha.1", "1.2.2"),
        ("1.2.0", "2.4.1+build44231"),
        ("2.1.0-beta", "2.1.0b"),
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), f"lt failed: {left} < {right}"
        assert Version(right) > Version(left), f"gt failed: {right} > {left}"
        assert Version(left) != Version(right), f"neq failed: {left} != {right}"

        assert Version(left) <= Version(right), f"le failed: {left} <= {right}"
        assert Version(right) >= Version(left), f"ge failed: {right} >= {left}"
        assert Version(left) == Version(right), f"eq failed: {left} == {right}"


if __name__ == "__main__":
    main()