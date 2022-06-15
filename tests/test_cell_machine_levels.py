import cell_machine_levels, unittest


class TestLevel(unittest.TestCase):
    def test_open(self):
        test = cell_machine_levels.level.Level(10, 10, "", "test", 2)
        test[0, 0] = True
        test[1, 0] = cell_machine_levels.level.Cell(
            cell_machine_levels.level.CellEnum.mover,
            cell_machine_levels.level.Rotation.up,
        )
        self.assertEqual(
            test, cell_machine_levels.level.open("V1;10;10;0.0;3.3.1.0;test;2")
        )
        self.assertEqual(
            test, cell_machine_levels.level.open("V2;a;a;}Y;;test;2")
        )

    def test_save(self):
        test = cell_machine_levels.level.Level(10, 10, "", "test", 2)
        test[0, 0] = True
        test[1, 0] = cell_machine_levels.level.Cell(
            cell_machine_levels.level.CellEnum.mover,
            cell_machine_levels.level.Rotation.up,
        )
        self.assertEqual(test.save("V1"), "V1;10;10;0.0;3.3.1.0;test;2")
        self.assertEqual(test.save("V2"), "V2;a;a;}Y;;test;2")


if __name__ == "__main__":
    unittest.main()
