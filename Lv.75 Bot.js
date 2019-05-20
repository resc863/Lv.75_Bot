function response(room, msg, sender, isGroupChat, replier, ImageDB) { 
      name = msg.split(" ")
      if(name[0] == "레식")  {
        var u = Utils.getWebText("https:/"+"/r6.tracker.network/profile/pc/"+name[1]);
        var t = u.split("<div class=\"trn-defstat__value\">");
        replier.reply(name[1] + "님의 레인보우 식스 전적 검색결과 입니다\n레벨 : " + t[0]+ "\n랭크 : " + t[2] +"\nMMR : " + t[1] +"\n승률 : " + t[6] + "\n킬뎃 : " + t[8];
      }
}
