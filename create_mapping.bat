# Copy and paste this into the kibana console
# Dev Tools -> Console

PUT lifts
{}

PUT lifts/_mapping/lifting_set 
{
  "properties": {
    "date": {
      "type": "date",
      "format": "MM/dd/YY"
    },
    "exercise": {
      "type": "text",
      "fields": {
        "raw": {
          "type": "keyword"
        }
      }
    },
    "weight": {
      "type": "integer"
    }
  }
}
