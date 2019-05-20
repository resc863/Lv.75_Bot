function response(room, msg, sender, isGroupChat, replier, ImageDB) { 
try {
        if(msg.indexOf("레식") == 0)  {
        var u = Utils.getWebText("https://r6.tracker.network/profile/pc/"+msg.substr(2));
        var t = u.split("<div class=\"trn-defstat__value\">");
        replier.reply(msg.substr(2) + "님의 레인보우 식스 전적 검색결과 입니다\n레벨 : " + t[0].split("<")[0]+ "\n랭크 : " + t[2].split("<")[0] +"\nMMR : " + t[1].split("<")[0] +"\n승률 : " + t[6].split("<")[0]);\n킬뎃 : " + t[8].split("<")[0]);
        }
      }    catch(e) {
      replier.reply("레식 전적 정보가 없습니다");
  }
}
