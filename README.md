# rfit
![Picture of RFIT dashboard](https://github.com/runt1me/rfit/raw/master/rfit_dashboard.png)

Here is a system I created for tracking and charting my workouts. Although there are a zillion fitness tracking apps out there,
I decided to make my own rather than sift through the masses of fitness tracking systems that probably
contained lots of extraneous features.

### The system keeps track of:
+ Progress in specific lifts over time
+ Adjusted one-rep maxes for various lifts, even if you haven't performed a one-rep max
+ Number of lifts per day

## How to use
![Picture of Workout Log](https://github.com/runt1me/rfit/raw/master/small_workout_log.PNG)
+ Log workouts in notes app in accordance with the current supported logging format
+ Ingest the raw text of the note into the parsing script
+ Send the output of the parsing script to an [elasticsearch](https://www.elastic.co/) backend running on `localhost:9200`.
+ Configure a [Kibana](https://www.elastic.co/products/kibana) dashboard to be populated by the elasticsearch backend.
+ Navigate to `localhost:5601` in your web browser.

