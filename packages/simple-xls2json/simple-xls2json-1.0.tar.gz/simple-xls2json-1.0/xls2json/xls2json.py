import xlrd

class Xls2Json:
    def __init__(self):
        pass

    def setConfig(self, config):
        self.config = config

    def getPageCount(self, file):
        names = file.sheet_names()
        return len(names)

    def buildPageInfo(self, name, sheet):
        list = []
        endline = sheet.nrows if self.config.endLine == -1 else self.config.endLine
        for i in range(self.config.startLine, endline):
            row = sheet.row_values(rowx = i)
            values = {}
            for (index, key) in self.config.def_values:
                if index < len(row):
                    values[key] = row[index]
            list.append(values)
        return {
            'name': name,
            'lines': list
        }

    def buildPageList(self, file):
        names = file.sheet_names()
        list = []
        for name in names:
            list.append(self.buildPageInfo(name, file.sheet_by_name(sheet_name=name)))
        return list

    def toJson(self, path):
        file = xlrd.open_workbook(path)
        return {
            'code': 0,
            'pageCount': self.getPageCount(file),
            'pages': self.buildPageList(file)
        }

class Config:
    def __init__(self):
        self.startLine = 0
        self.endLine = -1
        self.def_values = []
    
    def start(self, startLine):
        self.startLine = startLine
        return self

    def end(self, endLine):
        self.endLine = endLine
        return self

    def values(self, values):
        self.def_values = values
        return self

    def value(self, index, name):
        self.def_values.append((index, name))
        return self