import cell_machine_levels, unittest


class TestLevel(unittest.TestCase):
    def test_open(self):
        test = cell_machine_levels.level.Level(10, 10, "test", 2)
        test[0, 0] = True
        test[0, 1] = cell_machine_levels.level.Cell(
            cell_machine_levels.level.CellEnum.mover,
            cell_machine_levels.level.Rotations.up,
        )
        test1 = cell_machine_levels.level.open("V1;10;10;0.0;3.3.0.1;test;2")
        self.assertEqual(test, test1)


if __name__ == "__main__":
    unittest.main()
