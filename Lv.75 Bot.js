var json = getWebText("https://api.r6stats.com/api/v1/players/"+name+"/?platform=uplay")

var data =JSON.parse(json)

var lvl = data.find
