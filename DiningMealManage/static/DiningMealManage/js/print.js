function doPrint() {
        //打开一个新的窗体
      var bdhtml=window.document.body.innerHTML;
    var newWin = window.open('about:blank',"","");
        //取得id为"order"的<div id="order"></div>之间的内容
       //将取得的打印内容放入新窗体
    newWin.document.write(bdhtml);
       //刷新新窗体
    newWin.document.location.reload();
  //调用打印功能
    newWin.print();
       //打印完毕自动关闭新窗体
    newWin.close();
    //window.location='/DiningMealManage/pushPage/';
}/**
 * Created by acer on 2016/1/29.
 */
