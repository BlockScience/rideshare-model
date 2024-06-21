```
+-------------------------+
| Start Handling Ride     |
| Request Event           |
+------------+------------+
             |
             v
+------------+------------+
| Check First Available   |
| Driver                  |
+------------+------------+
             |
             v
+------------+------------+
| Will Driver Accept Ride?|
| (Calculate Acceptance   |
| Threshold)              |
+---------+--+------------+
          |Yes|               No
          v   |              v
+---------+---+----------+ +-------------------+
| Calculate Travel Time  | | Log Decline and   |
| and Cost               | | Check Next        |
+---------+---+----------+ | Available Driver  |
          |                +--------+----------+
          v                         |
+---------+---+----------+          |
| Assign Driver to Ride  |          |
| and Update States      |          |
+---------+---+----------+          |
          |                         |
          v                         |
+---------+---+----------+          |
| Push Event: Driver     |          |
| Assigned               |          |
+---------+---+----------+          |
          |                         |
          v                         |
+---------+---+----------+          |
| End Handling Ride      |          |
| Request Event          |          |
+---------+---+----------+          |
          |                         |
          v                         |
+---------+---+----------+          |
| All Drivers Checked?   |          |
+--------+---+-----------+          |
         |No |              Yes     |
         v   |              v       |
+--------+---+-----------+ +--------+----------+
| Check Next Driver      | | No Driver         |
| (Loop Back to "Will    | | Available         |
| Driver Accept Ride?")  | | (Retry After      |
+--------+---+-----------+ | Delay)            |
         |                 +--------+----------+
         v                          |
+--------+---+-----------+          |
| Push Event: Request    |          |
| Ride to Retry Queue    |          |
+--------+---+-----------+          |
         |                          |
         v                          |
+--------+---+-----------+          |
| End Handling Ride      |          |
| Request Event          |          |
+--------+---+-----------+          |

```


