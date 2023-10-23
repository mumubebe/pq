# 📎️ pq-json
pq is a Python command-line JSON processor - **almost** like (atleast inspired by 🐶️) [jq](https://github.com/stedolan/jq), but using Python focusing on simplicity and convenience with familiar syntax.

## Install
```
pip install pq-json
```


Here is a simple example for parsing JSON. Output from pq is pretty printed using [Rich](https://github.com/Textualize/rich).
```
$ echo '{"text": "Text here", "header": "Header", "list": [1,2,3]}' | pq
{
  "text": "Text here",
  "header": "Header",
  "list": [
    1,
    2,
    3
  ]
}

#j represents the current input object in a filter.
echo '{"text": "Text here", "header": "Header", "list": [1,2,3]}' | pq 'j["list"] | j * 4'
4
8
12
```

### Filters
The processing is handled with filters, like in jq.
j represents the current input object in a filter. 
```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j['example']"
"data"
```

```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j['example']"
"data"
```

As default, None will not be passed.
```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j.get('nada')"

```

### List slicing

JSON arrays are converted to Python list. 
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[0]"
{
  "name": "eric",
  "age": 22
}
```
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[-1]"
{
  "name": "daniel",
  "age": 44
}
```

An array always iterates to the next filter. Here we are using the slice symbol [:] to highlight that we are working with an array. 
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[:]"
{
  "name": "eric",
  "age": 22
}
{
  "name": "daniel",
  "age": 44
}
```



### Pipes
Pipes let you chain multiple filters by produce output to the filter to the right of the pipe. Under the hood a pipeline is a chain of generators. An array will for example yield multiple elements to the right. 

input: 
```json
["a", "b", "c", "d"]
```
```
pq "j[0:2] | j.upper()"
      |         |
   filter1   filter2

produces the following result:
"A"
"B"

In this case, the expression j.upper() will be run each time.

j[0] -> "a".upper() -> "A"
j[1] -> "b".upper() -> "B"

Another example:

$ echo '[1,2,3,4,5,6,7,8,9]' | pq 'j[:] | j**2+50'
51
54
59
66
75
86
99
114
131
```
### Array constructs
Above example outputs a list of integers. It's possible to accumulate data into an array. Use the flag ```-a``` after the pipe sign, like this:
```
$ echo '[1,2,3,4,5]' | pq "j[:] | -a max(j)"
5
```
Here is another example:
```
$ echo '[1,2,3,4,5,6,7,8,9]' | pq 'j[:] | j**2+50 | -a [j]'
[51, 54, 59, 66, 75, 86, 99, 114, 131]
```
### Object constructs
```
$ echo '{"name":"jan", "age":4, "parents": ["lisa", "dan"]}' | pq '{"name": j["name"], "parents": j["parents"]}'
{
  "name": "jan",
  "parents": [
    "lisa",
    "dan"
  ]
}
```
### Custom modules

It's possible to add additional modules to global scope from file or input string.

We can declare a variable for example.
```
$ echo '[1,2,3]' | pq --module 'two=2' 'j[1]*two'
4
```



### Other examples

We can easily use built-in functions in Python
```
$ echo "[1,2,3,4,5,6]" | pq 'sum(j) | {"total": j}'
{
  "total": 21
}
```
