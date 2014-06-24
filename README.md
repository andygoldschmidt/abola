spalter
=====
[![Build Status](https://travis-ci.org/andygoldschmidt/spalter.svg?branch=master)](https://travis-ci.org/andygoldschmidt/spalter)

Frequentist A/B testing.


## Example

```
from spalter.trial import Trial
t = Trial(['test', 'control'], ['conversion_rate'])
t.update({'conversion_rate': {'test': [0, 1, 0, 1], 'control: [0, 1, 0, 0]}})
t.evaluate('mean')
```

## Acknowledgements

Heavily inspired by [trials](https://github.com/bogdan-kulynych/trials).
