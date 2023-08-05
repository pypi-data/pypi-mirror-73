## Introduction

+ This is an Open-Source Project intended to aid the developers in the Healthcare Industry.
+ This package helps you to get the ICD-10 Code's Description when provided with a ICD-10 Code/ICD-10 Codes List

## How To Use

+ Install using `pip install icd10-c2d`
+ Import using `from icd10.code2description import Code2Description as c2d`
+ Get ICD Code's Description using `c2d.getICDDescription(["ICD10 Code 1","ICD10 Code 2","ICD10 Code N"])`
+ Finally, it looks like this :

```
from icd10.code2description import Code2Description as c2d
c2d.getICDDescription(["ICD10 Code 1","ICD10 Code 2","ICD10 Code N"])
```

+ Returns you a Map of ICD Codes with their Descriptions.

> Note : All the imports/dependencies are automatically installed.

## Bugs & Issues

+ If you find a Bug or have an Idea, please feel free to drop a mail @ sakethaux1111@gmail.com!
