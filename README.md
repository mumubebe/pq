# pq
pq is a Python command-line JSON processor - **almost** like jq, but using Python

```
python -m pip install git+https://github.com/mumubebe/pq.git
```



```
$ echo '"This is a string"' | pq
"This is a string"
```


```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j['example']"
"data"
```

```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j['example']"
"data"
```

```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j.get('nada')"

```

*** List slicing ***
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[0]"
{
  "name": "eric",
  "age": 22
}

$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[-1]"
{
  "name": "daniel",
  "age": 44
}
```

***Pipe***

```
echo '[{"name": "eric", "siblings": ["lena"]}, {"name": "daniel", "siblings": ["jan", "julia"]}]' | pq "j[:] | j['siblings']"
"lena"
"jan"
"julia"
```