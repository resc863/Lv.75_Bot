function response(room, msg, sender, isGroupChat, replier, ImageDB) { //모르면 첫번째 강좌 보고오세요
try {//예외처리
        if(msg.indexOf("/롤전적") == 0)  {//메세지가 롤전적일때
        var u = Utils.getWebText("http://www.op.gg/summoner/userName="+msg.substr(4));//변수 u는 이링크를 HTML파싱한 값이다
        var t = u.split("<span class=\"tierRank\">");//변수 a는 변수 u에서 HTML에 <span class="tierRank"> 을 자른값 입니다 /이걸로 해서 tierRank부분을 자른겁니다
        var w = u.split("<span class=\"wins\">");//나머지도 마찬가지입니다
        var l = u.split("<span class=\"losses\">");
        var win = u.split("<span class=\"winratio\">");
        replier.reply(msg.substr(4) + "님에 롤 전적 검색결과 입니다\n티어 : " + t[1].split("<")[0]+ "\n승리 : " + w[1].split("<")[0] +"\n패배 : " + l[1].split("<")[0] +"\n승률 : " + win[1].split("<")[0]);
//버구칠 블로그 참조!
        }
      }    catch(e) {//결과값을 찾을수 없으면
      replier.reply("롤전적 정보가 없습니다");
  }
}
