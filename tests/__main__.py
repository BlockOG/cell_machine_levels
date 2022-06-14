import cell_machine_levels, unittest


class TestLevel(unittest.TestCase):
    def test_open(self):
        test = cell_machine_levels.level.Level(10, 10, "test", 2)
        test[0, 0, True] = True
        test[0, 1, False] = cell_machine_levels.level.Cell(
            cell_machine_levels.level.CellEnum.mover,
            cell_machine_levels.level.CellEnum.rotation.up,
        )
        self.assertEqual(
            test, cell_machine_levels.level.open("V1;10;10;0.9;3.3.0.8;test;2")
        )


if __name__ == "__main__":
    unittest.main()
