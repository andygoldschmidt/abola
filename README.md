abola
=====
![](https://travis-ci.org/andygoldschmidt/abola.svg?branch=master)

Frequentist A/B testing.


## Example

```
from trial import Trial
t = Trial(['test', 'control'], ['conversion_rate'])
t.update({'conversion_rate': {'test': [0, 1, 0, 1], 'control: [0, 1, 0, 0]}})
t.evaluate('mean')
```
