#! /usr/bin/env python
#coding=utf8


import os.path
import xlrd

class ParseXls(object):
    """
    Parse Xls
    """
    filename = None
    isrow = True

    def __init__(self, filename, isrow):
        self.filename = filename
        self.isrow = isrow

    """
    read an xls
    """
    def readXls(self):
        if not self.getXlsSheet(): return False
        sheet = self.getXlsSheet()
        book_list = []
        if self.isrow:
            # get nrows data
            nrows = sheet.nrows
            for i in xrange(0,nrows):
                row_data = sheet.row_values(i)
                book_list.append(row_data)
        else:
            # get ncols data
            ncols = sheet.ncols
            for i in xrange(0,ncols):
                col_data = sheet.col_values(i)
                book_list.append(col_data)

        return book_list

    """
    write an xls
    ctype: 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    xf: extension of the formatting(default 0)
    this function is unavailable
    """
    def writeXls(self, x, y, ctype, value, xf):
        x = int(x)
        y = int(y)
        if not self.getXlsSheet(): return False
        sheet = self.getXlsSheet()
        new_cell = sheet.put_cell(x, y, ctype, value, xf)

    def getCell(self, x, y):
        x = int(x)
        y = int(y)
        if not self.getXlsSheet(): return False
        sheet = self.getXlsSheet()
        nrows = sheet.nrows
        ncols = sheet.ncols
        print "nrows:{},ncols:{}".format(nrows, ncols)
        if x > nrows or y > ncols:
            print "x:{} need lt nrows:{}, y:{} need lt ncols:{}".format(x, nrows, y, ncols)
            return False
        return sheet.cell_value(x, y)
        # return sheet.cell(x, y).value

    """
    get an xls sheet
    """
    def getXlsSheet(self):
        if not self.filename:
            print "no xls file!"
            return False

        ext = os.path.splitext(self.filename)[1]
        # print ext
        # print ext != '.xls' or ext != '.xlsx'
        if not ext in ['.xls', '.xlsx']:
            print "filename {} invalid format".format(self.filename)
            return False

        # print "xls file: {}".format(self.filename)
        # open xls file
        xlsfile = self.filename
        book = xlrd.open_workbook(xlsfile)
        # get the first sheet_name of xlsfile 
        sheet_name = book.sheet_names()[0]
        try:
            # get sheet
            sheet = book.sheet_by_name(sheet_name)
            return sheet
        except Exception, e:
            print e
            return False

        