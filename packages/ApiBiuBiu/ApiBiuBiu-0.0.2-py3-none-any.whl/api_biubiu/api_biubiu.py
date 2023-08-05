# coding=utf-8

__author__ = "满眼乱世妖娆"
__version__ = "0.0.1"

try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO
import unittest, time, sys, datetime
from multiprocessing import Pool, Lock

# from xml.sax import saxutils

try:
  reload(sys)
  sys.setdefaultencoding('utf-8')
except NameError:
  pass


class OutputRedirector(object):
  """ Wrapper to redirect stdout or stderr """

  def __init__(self, fp):
    self.fp = fp

  def write(self, s):
    self.fp.write(s)

  def writelines(self, lines):
    self.fp.writelines(lines)

  def flush(self):
    self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

TestResult = unittest.TestResult


class _TestResult(TestResult):
  # note: _TestResult is a pure representation of results.
  # It lacks the output and reporting ability compares to unittest._TextTestResult.

  def __init__(self, verbosity=1):
    TestResult.__init__(self)
    self.stdout0 = None
    self.stderr0 = None
    self.success_count = 0
    self.failure_count = 0
    self.error_count = 0
    self.verbosity = verbosity
    # sdsdsdsdsdsdsdsdsdsds
    import io
    self.outputBuffer = io.StringIO()
    self.test_start_time = round(time.time(), 2)
    self.result = []

  def startTest(self, test):
    TestResult.startTest(self, test)
    # just one buffer for both stdout and stderr
    self.outputBuffer = StringIO()
    stdout_redirector.fp = self.outputBuffer
    stderr_redirector.fp = self.outputBuffer
    self.stdout0 = sys.stdout
    self.stderr0 = sys.stderr
    sys.stdout = stdout_redirector
    sys.stderr = stderr_redirector

  def complete_output(self):
    """
    Disconnect output redirection and return buffer.
    Safe to call multiple times.
    """
    if self.stdout0:
      sys.stdout = self.stdout0
      sys.stderr = self.stderr0
      self.stdout0 = None
      self.stderr0 = None
    return self.outputBuffer.getvalue()

  def stopTest(self, test):
    # Usually one of addSuccess, addError or addFailure would have been called.
    # But there are some path in unittest that would bypass this.
    # We must disconnect stdout in stopTest(), which is guaranteed to be called.
    self.complete_output()

  def addSuccess(self, test):
    self.success_count += 1
    TestResult.addSuccess(self, test)
    output = self.complete_output()
    self.result.append((0, test, output, ''))
    if self.verbosity > 1:
      # sys.stderr.write('ok')
      sys.stderr.write(str(test))
      # sys.stderr.write('\n')
    else:
      # sys.stderr.write('.')
      pass

  def addError(self, test, err):
    self.error_count += 1
    TestResult.addError(self, test, err)
    _, _exc_str = self.errors[-1]
    output = self.complete_output()
    self.result.append((2, test, output, _exc_str))
    if self.verbosity > 1:
      # sys.stderr.write('E  ')
      sys.stderr.write(str(test))
      # sys.stderr.write('\n')
    else:
      # sys.stderr.write('E')
      pass

  def addFailure(self, test, err):
    self.failure_count += 1
    TestResult.addFailure(self, test, err)
    _, _exc_str = self.failures[-1]
    output = self.complete_output()
    self.result.append((1, test, output, _exc_str))
    if self.verbosity > 1:
      # sys.stderr.write('F  ')
      sys.stderr.write(str(test))
      sys.stderr.write('\n')
    else:
      # sys.stderr.write('F')
      pass


class ReportSource(object):
  # 写头部
  ReportHeader = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>%(MultithreadingTestReport)s</title>
  <meta name="generator" content="HTMLTestReportCN 0.8.3"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
  <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
  <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
  <style type="text/css" media="screen">\n"""

  ReportHeaderCSS = """    body {
      font-family: Microsoft YaHei, Tahoma, arial, helvetica, sans-serif;
      padding: 20px;
      font-size: 100%;
    }

    table {
      font-size: 100%;
    }

    /* -- heading ---------------------------------------------------------------------- */
    .heading {
      margin-top: 0ex;
      margin-bottom: 1ex;
    }

    .heading .description {
      margin-top: 4ex;
      margin-bottom: 6ex;
    }

    /* -- report ------------------------------------------------------------------------ */
    #total_row {
      font-weight: bold;
    }

    .passCase {
      color: #5cb85c;
    }

    .failCase {
      color: #d9534f;
      font-weight: bold;
    }

    .errorCase {
      color: #f0ad4e;
      font-weight: bold;
    }

    .hiddenRow {
      display: none;
    }

    .testcase {
      margin-left: 2em;
    }
  </style>
</head>\n"""

  ReportSummary = """<body>
<div class='heading'>
  <h1 style="font-family: Microsoft YaHei">%(MultithreadingTestReport)s</h1>
  <p class='attribute'><strong>测试人员 : </strong> %(Tester)s </p>
  <p class='attribute'><strong>开始时间 : </strong> %(StartTime)s</p>
  <p class='attribute'><strong>合计耗时 : </strong> %(TotalTime)s</p>
  <p class='attribute'><strong>测试结果 : </strong> %(TestResult)s</p>
  <p class='description'></p>
</div>\n"""

  ReportCaseSummary = """<p id='show_detail_line'>
  <a class="btn btn-primary" href='javascript:showCase(4)'> %(PassRate)s</a>
  <a class="btn btn-success" href='javascript:showCase(0)'> %(PassNum)s</a>
  <a class="btn btn-danger" href='javascript:showCase(2)'> %(fail)s</a>
  <a class="btn btn-info" href='javascript:showCase(3)'> %(CaseNum)s</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
  <col align='left' />
  <col align='right' />
  <col align='right' />
  <col align='right' />
  <col align='right' />
</colgroup>
<tr id='header_row' class="text-center active" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>点击查看</td>
</tr>\n"""

  # 写每一个case头部
  ReportSuccessCaseSummary = """<tr class='success'>
  <td>%(TestName)s</td>
  <td class="text-center">%(Total)s</td>
  <td class="text-center">%(Pass)s</td>
  <td class="text-center">%(Fail)s</td>
  <td class="text-center"><a href="javascript:showClassDetail('%(CaseSequence)s',%(CountCase)s)" class="detail" id='%(CaseSequence)s'>点击查看</a></td>
</tr>\n"""

  ReportFailCaseSummary = """<tr class='warning'>
  <td>%(TestName)s</td>
  <td class="text-center">%(Total)s</td>
  <td class="text-center">%(Pass)s</td>
  <td class="text-center">%(Fail)s</td>
  <td class="text-center"><a href="javascript:showClassDetail('%(CaseSequence)s',%(CountCase)s)" class="detail" id='%(CaseSequence)s'>点击查看</a></td>
</tr>\n"""

  ReportSuccessCases = f"""<tr id='pt%(DivNumber)s' class='hiddenRow'>
    <td class='passCase'><div class='testcase'>%(CaseName)s</div></td>
    <td colspan='5' align='center'>
    <button id='btn_pt1_1' type="button"  class="btn-xs btn btn-success" data-toggle="collapse" data-target='#div_pt%(DivNumber)s'>通过</button>
    <div id='div_pt%(DivNumber)s' class="collapse in">
    <pre>

%(Detail)s

    </pre>
    </div>
    </td>
</tr>\n"""


  ReportFailureCases = f"""<tr id='et%(DivNumber)s' class='none'>
    <td class='errorCase'><div class='testcase'>%(CaseName)s</div></td>
    <td colspan='5' align='center'>
    <button id='btn_et1_1' type="button"  class="btn-xs" data-toggle="collapse" data-target='#div_et%(DivNumber)s'>失败</button>
    <div id='div_et%(DivNumber)s' class="collapse in">
<pre>

%(Detail)s

</pre>
</div>
</td>
</tr>\n"""

  ReportFloatNum = """<tr id='total_row' class="text-center info">
    <td>总计</td>
    <td>%(CaseNum)s</td>
    <td>%(PassNum)s</td>
    <td>%(fail)s</td>
    <td>%(PassRate)s</td>
</tr>
</table>\n"""

  ReportJSCode = """<div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
  <a href="#"><span class="glyphicon glyphicon-eject" style="font-size:30px;" aria-hidden="true">
    </span></a></div>

<script language="javascript" type="text/javascript">
    output_list = Array();
    $("button[id^='btn_pt']").addClass("btn btn-success");
    $("button[id^='btn_ft']").addClass("btn btn-danger");
    $("button[id^='btn_et']").addClass("btn btn-warning");

    /*level
    增加分类并调整，增加error按钮事件 --Findyou v0.8.2.3
    0:Pass    //pt none, ft hiddenRow, et hiddenRow
    1:Failed  //pt hiddenRow, ft none, et hiddenRow
    2:Error    //pt hiddenRow, ft hiddenRow, et none
    3:All     //pt none, ft none, et none
    4:Summary //all hiddenRow
    */

    //add Error button event --Findyou v0.8.2.3
    function showCase(level) {
        trs = document.getElementsByTagName("tr");
        for (var i = 0; i < trs.length; i++) {
            tr = trs[i];
            id = tr.id;
            if (id.substr(0, 2) == 'ft') {
                if (level == 0 || level == 2 || level == 4) {
                    tr.className = 'hiddenRow';
                } else {
                    tr.className = '';
                }
            }
            if (id.substr(0, 2) == 'pt') {
                if (level == 1 || level == 2 || level == 4) {
                    tr.className = 'hiddenRow';
                } else {
                    tr.className = '';
                }
            }
            if (id.substr(0, 2) == 'et') {
                if (level == 0 || level == 1 || level == 4) {
                    tr.className = 'hiddenRow';
                } else {
                    tr.className = '';
                }
            }
        }

        //加入【详细】切换文字变化 --Findyou
        detail_class = document.getElementsByClassName('detail');
        //console.log(detail_class.length)
        if (level == 3) {
            for (var i = 0; i < detail_class.length; i++) {
                detail_class[i].innerHTML = "点击收起"
            }
        } else {
            for (var i = 0; i < detail_class.length; i++) {
                detail_class[i].innerHTML = "点击查看"
            }
        }
    }

    //add Error button event --Findyou v0.8.2.3
    function showClassDetail(cid, count) {
        var id_list = Array(count);
        var toHide = 1;
        for (var i = 0; i < count; i++) {
            tid0 = 't' + cid.substr(1) + '_' + (i + 1);
            tid = 'f' + tid0;
            tr = document.getElementById(tid);
            if (!tr) {
                tid = 'p' + tid0;
                tr = document.getElementById(tid);
            }
            if (!tr) {
                tid = 'e' + tid0;
                tr = document.getElementById(tid);
            }
            id_list[i] = tid;
            if (tr.className) {
                toHide = 0;
            }
        }
        for (var i = 0; i < count; i++) {
            tid = id_list[i];
            //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
            if (toHide) {
                document.getElementById(tid).className = 'hiddenRow';
                document.getElementById(cid).innerText = "点击查看"
            } else {
                document.getElementById(tid).className = '';
                document.getElementById(cid).innerText = "点击收起"
            }
        }
    }

    function html_escape(s) {
        s = s.replace(/&/g, '&amp;');
        s = s.replace(/</g, '&lt;');
        s = s.replace(/>/g, '&gt;');
        return s;
    }
</script>
</body>
</html>\n"""




"""
霸气的包名：Api_BiuBiu
stream：报告路径，str属性，不要用 with open
verbosity:报告等级，命令行展示内容我清空了。此参数用处不大
title:报告title
executor:执行人名字
"""
class Api_BiuBiu(ReportSource):

  def __init__(self, stream="测试报告.html", verbosity=1, title=None, executor=None):
    self.stream = stream
    self.verbosity = verbosity
    self.title = title if title else "多线程_测试报告"
    self.executor = str(executor) if executor else "外星人"
    self.startTime = str(datetime.datetime.now())
    self.Test_consuming = 0
    self.EveryCaseResults = {}
    self.ReportInformation = {}
    self.caseInformation = {}
    self.bottom = {}

  """
  根据是否有addTest属性判断是TestSuite还是class
  然后启动多进程，列表多长启动多少进程，为了快
  因为python的PLI全局解释锁，所以用进程，不用线程
  """

  def RunEveryCase(self, test):
    if not isinstance(test, list):
      print("\n为啥不传给我列表 ? 淘气 ～～～")
      exit(1)
    if len(test) <= 0:
      print("\n进程都准备好了你给我空列表 ？ 不乖～～～")
      exit(1)

    work_list = []
    pool = Pool(processes=len(test))
    for i in test:
      if hasattr(i, 'addTest'):
        work_list.append(pool.apply_async(func=self.WorkingProcess, args=(i,)))
      else:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(i))
        work_list.append(pool.apply_async(func=self.WorkingProcess, args=(suite,)))
    pool.close()
    pool.join()
    for n in work_list:
      self.ClassIfication(n.get())
    self.GenerateReport()

  """
  结果归类方便写入html
  """

  def ClassIfication(self, Result):
    self.Test_consuming += Result[0]
    Sign = None
    for case in Result[1]:
      CaseName = str(case[1]).split()[1][1:-1]
      if not self.EveryCaseResults.get(CaseName):
        self.EveryCaseResults[CaseName] = []
        Sign = CaseName
        self.EveryCaseResults[CaseName].append(case)
      else:
        if Sign == CaseName:
          self.EveryCaseResults[CaseName].append(case)
        else:
          self.EveryCaseResults[CaseName] = []
          Sign = CaseName
          self.EveryCaseResults[CaseName].append(case)

  """
  这里是核心的多进程执行方法
  把执行结果返回给主进程进行统计
  """

  def WorkingProcess(self, test):
    start_time = datetime.datetime.now()
    result = _TestResult(self.verbosity)
    test(result)
    end_time = datetime.datetime.now()
    return (end_time - start_time).seconds, result.result

  def Statistics(self):
    fail = 0
    success = 0
    for k, y in self.EveryCaseResults.items():
      for i in y:
        if i[0] == 0:
          success += 1
        else:
          fail += 1
    CaseNum = sum([success, fail])
    PassRate = round((success / sum([success, fail])) * 100, 2)
    TestResult = f"共{CaseNum}，通过{success}，错误{fail}，通过率 = {PassRate} %"

    ReportInformation = {"Tester": self.executor, "StartTime": self.startTime,
                         "TotalTime": f"{self.Test_consuming} 秒 （每个进程时间的和）",
                         "TestResult": TestResult,"MultithreadingTestReport":self.title}
    caseInformation = {"CaseNum": f"所有数量: {CaseNum}", "PassNum": f"通过数量: {success}", "fail": f"失败数量: {fail}",
                       "PassRate": f"通过率: {PassRate}%"}
    bottom = {"CaseNum": f"{CaseNum}", "PassNum": f"{success}", "fail": f"{fail}", "PassRate": f"{PassRate}%"}
    self.ReportInformation = ReportInformation
    self.caseInformation = caseInformation
    self.bottom = bottom

  def PassRateOfTest(self, OneTest):
    Pass = 0
    Fail = 0
    for i in OneTest:
      if i[0] == 0:
        Pass += 1
      else:
        Fail += 1
    PassOrNot = r"warning" if Fail > 0 else r"success"
    Information = {"Total": f"{sum([Pass, Fail])}", "Pass": f"{Pass}", "Fail": f"{Fail}",
                   "CountCase": f"{len(OneTest)}", "PassOrFail": PassOrNot}
    return Information

  def GenerateReport(self):
    self.Statistics()
    SuiteNmuber = 0
    with open(file=self.stream, mode="w", encoding="utf-8")as f:
      f.write(self.ReportHeader % {"MultithreadingTestReport":self.title})
      f.write(self.ReportHeaderCSS)
      f.write(self.ReportSummary % self.ReportInformation)
      f.write(self.ReportCaseSummary % self.caseInformation)
      for k, y in self.EveryCaseResults.items():
        SuiteNmuber += 1
        CaseNumber = 0
        OneCase = self.PassRateOfTest(y)
        OneCase["TestName"] = k
        OneCase["CaseSequence"] = f"c{SuiteNmuber}"
        if OneCase["PassOrFail"] == "success":
          del OneCase["PassOrFail"]
          f.write(self.ReportSuccessCaseSummary % OneCase)
        else:
          del OneCase["PassOrFail"]
          f.write(self.ReportFailCaseSummary % OneCase)

        for i in y:
          CaseNumber += 1
          CaseDetail = {"DivNumber": f"{SuiteNmuber}_{CaseNumber}", "CaseName": str(i[1]).split()[0], "Detail": f"{i[2]}\n{i[3]}"}
          if i[0] == 0:
            f.write(self.ReportSuccessCases % CaseDetail)
          else:
            f.write(self.ReportFailureCases % CaseDetail)
      f.write(self.ReportFloatNum % self.bottom)
      f.write(self.ReportJSCode)
    print("\n-----------")
    print('报告生成成功')
