from json import dumps, loads

x = [{
    "a": 3,
    "b": 4
},
{
    3: "a",
    4: "b"
}]

with open("test.json", "w") as f:
    f.write(dumps(x, indent = 4))   