""" Some basic sanity testing for otto and utils """

import unittest

from utils import get_waypoints, get_pathmap, init_map
from otto import get_neighbors, cost, find_best_time

class TestOtto(unittest.TestCase):

    def test_getwaypoints(self):

        gwp = get_waypoints

        self.assertEqual(
                gwp([]), {}
        )
        self.assertEqual(
                gwp(['10 20 30']),
                {0: {'penalty': 0, 'coord': (0, 0)}, 1: {'penalty': 30, 'coord': (10, 20)}, 2: {'penalty': 0, 'coord': (100, 100)}} 
        )

    def test_pathmap(self):

        gpm = get_pathmap

        self.assertEqual(
            gpm(0),
            {0: None, 1: None}
        )

        self.assertEqual(
            gpm(3),
            {0: None, 1: None, 2: None, 3: None, 4: None}
        )

    def test_get_neighbors(self):

        gn = get_neighbors

        points = { 0: None }
        self.assertEqual(gn(0, points), [])

        points = { 0: None, 1: None }
        self.assertEqual(gn(0, points), [1])

        points = { 0: None, 1: None,  3: None, -1: None}
        self.assertEqual(gn(1, points), [3])

    def test_cost(self):

        points = {
            0:  { 'coord' : (0, 0), 'penalty': 0},
            1:  { 'coord':  (50, 50), 'penalty': 50},
            2:  { 'coord':  (10, 90), 'penalty': 0},
            3:  { 'coord':  (100, 100), 'penalty': 0}
        }

        cost1 = cost(0, 1, points)
        cost2 = cost(0, 2, points)

        self.assertTrue(cost1 < cost2)

        cost3 = cost(0, 3, points)
        cost4 = cost(0, 2, points)

        self.assertTrue(cost4 < cost3)


    def test_find_best_time(self):
        fbt = find_best_time

        pathmap1 = {0: None, 1: None, 2: None }
        points1 = {
            0:  { 'coord' : (0, 0), 'penalty': 0},
            1:  { 'coord':  (50, 50), 'penalty': 20},
            2:  { 'coord':  (100, 100), 'penalty': 0},
        }
        init_map(0, points1, pathmap1, get_neighbors, cost)


        pathmap2 = {0: None, 1: None, 2: None, 3: None, 4: None }
        points2 = {
            0:  { 'coord' : (0, 0), 'penalty': 0},
            1:  { 'coord':  (30, 30), 'penalty': 90},
            2:  { 'coord':  (60, 60), 'penalty': 80},
            3:  { 'coord':  (10, 90), 'penalty': 100},
            4:  { 'coord':  (100, 100), 'penalty': 0}
        }
        init_map(0, points2, pathmap2, get_neighbors, cost)


        pathmap3 = {0: None, 1: None, 2: None, 3: None, 4: None }
        points3 = {
            0:  { 'coord' : (0, 0), 'penalty': 0},
            1:  { 'coord':  (30, 30), 'penalty': 90},
            2:  { 'coord':  (60, 60), 'penalty': 80},
            3:  { 'coord':  (10, 90), 'penalty': 10},
            4:  { 'coord':  (100, 100), 'penalty': 0}
        }
        init_map(0, points3, pathmap3, get_neighbors, cost)

        self.assertEqual(fbt(pathmap1, points1), 90.711)
        self.assertEqual(fbt(pathmap2, points2), 156.858)
        self.assertEqual(fbt(pathmap3, points3), 110.711)

if __name__ == '__main__':
    unittest.main()
