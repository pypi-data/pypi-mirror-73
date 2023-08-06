SAMPLE_SCRIPT_WITH_PARALLEL_EDGES = """
    PRAGMA foreign_keys=ON;
    INSERT INTO Files (filename) VALUES ('test.md');
    INSERT INTO Notes (id, title, filename) VALUES
        (0, 'root', 'test.md'),
        (1, 'src', 'test.md'),
        (2, 'dest', 'test.md');
    INSERT INTO Links (src, dest, annotation) VALUES
        (1, 2, 'annotation');
    INSERT INTO Aliases (id, owner, alias) VALUES
        (1, 0, '0a'),
        (2, 0, '0a1');
    INSERT INTO Sequences (prev, next) VALUES
        ('0a', '0a1');
"""

def sample_script():
    """Sample script to initialize mock database."""
    return """
    PRAGMA foreign_keys=ON;
    INSERT INTO Files (filename) VALUES ('test.md');
    INSERT INTO Notes (id, title, filename) VALUES
        (1, 'Note 1', 'test.md'),
        (2, 'Note 2', 'test.md'),
        (3, 'Note 3', 'test.md'),
        (4, 'Note 4', 'test.md'),
        (5, 'Note 5', 'test.md'),
        (6, 'Note 6', 'test.md'),
        (7, 'Note 7', 'test.md'),
        (8, 'Note 8', 'test.md'),
        (9, 'Note 9', 'test.md');
    -- i -> 2*i
    INSERT INTO Links (src, dest, annotation) VALUES
        (1, 2, 'annotation'),
        (2, 4, 'annotation'),
        (3, 6, ''),
        (4, 8, '');
    INSERT INTO Aliases (id, owner, alias) VALUES
        (2, 1, '1a'),
        (3, 1, '1a1'),
        (4, 1, '1a2'),
        (6, 5, '5a'),
        (7, 5, '5a1'),
        (8, 5, '5a2'),
        (9, 5, '5a3');
    INSERT INTO Sequences (prev, next) VALUES
        ('1a', '1a1'),
        ('1a', '1a2'),
        ('5a', '5a1'),
        ('5a', '5a2'),
        ('5a', '5a3');
    """
