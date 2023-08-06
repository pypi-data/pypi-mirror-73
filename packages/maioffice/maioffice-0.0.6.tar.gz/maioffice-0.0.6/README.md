# Maishu Office package

基于python-docx和openpyxl一个简易的操作office套件的库

### 示例：
1. 读取word文档

```python
from maioffice import word
doc = word.load('sample.docx')
```

2. 替换word文档中的文字
```python
doc = word.load('sample.docx')
word.replace(doc, '旧的文字', '新的文字')
```

3. 读取excel文档
```python
from maioffice import excel
workbook = excel.load('sample.xlsx')
```
