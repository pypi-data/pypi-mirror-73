(this["webpackJsonpucess-talk-admin"]=this["webpackJsonpucess-talk-admin"]||[]).push([[12],{1012:function(e,t,a){"use strict";var n=a(0);t.a=function(e,t){var a=Object(n.useRef)();Object(n.useEffect)(function(){a.current=e},[e]),Object(n.useEffect)(function(){if(null!==t){var e=setInterval(function(){a.current()},t);return function(){return clearInterval(e)}}},[t])}},1187:function(e,t,a){},1265:function(e,t,a){"use strict";a.r(t);var n=a(10),r=a(20),l=a(0),c=a.n(l),i=a(7),o=a(174),s=a(38),d=a.n(s),m="[DASHBOARD APP] GET CONV LIST DATA",f="[DASHBOARD APP] GET CONV CHART1 DATA",u="[DASHBOARD APP] GET CONV CHART2 DATA",p="[DASHBOARD APP] GET STATISTICS",b="/api/conversations";function g(e,t){var a="";void 0!==t?a="offset=0&intent=&entity=&action=&policies=&exclude_self=true&"+Object.keys(t).map(function(e){return e+"="+t[e]}).join("&"):a="offset=0&intent=&entity=&action=&policies=&exclude_self=true";var n=d.a.get(b+"?"+a);return function(t){return n.then(function(a){"firstView"===e?t({type:f,payload:a.data}):"secondView"===e&&t({type:u,payload:a.data})})}}var x=a(46),y=a(12);function E(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),a.push.apply(a,n)}return a}function w(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?E(a,!0).forEach(function(t){Object(n.a)(e,t,a[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):E(a).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))})}return e}var h={statistics:null,conversations:null,conversationsChart:{firstView:null,secondView:null}},v=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:h,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case p:return w({},e,{statistics:t.payload});case m:return w({},e,{conversations:Object(y.a)(t.payload)});case f:return w({},e,{conversationsChart:w({},e.conversationsChart,{firstView:Object(y.a)(t.payload)})});case u:return w({},e,{conversationsChart:w({},e.conversationsChart,{secondView:Object(y.a)(t.payload)})});default:return e}},O=Object(x.d)({dashboard:v}),D=a(86),N=a.n(D),j=a(1012),Y=a(25),C=a(3),S=a(152),k=a(885),M=a(119),A=a(979);var P=c.a.memo(function(e){function t(e){return String(e).replace(/(\d)(?=(?:\d{3})+(?!\d))/g,"$1,")}return c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"p-16 pr-4 flex flex-row items-center"},c.a.createElement(k.a,{className:"mr-12"},"chat"),c.a.createElement(M.a,{className:"h3 font-bold"},"\uc804\uccb4 \uba54\uc2dc\uc9c0 \ud604\ud669")),c.a.createElement("div",{className:"text-center pt-12 pb-28"},c.a.createElement(M.a,{component:"div",className:"text-48 leading-none text-blue inline-flex"},c.a.createElement(A.Random,{text:String(t(e.widget.user_messages)),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"}),"\xa0/\xa0",c.a.createElement(A.Random,{text:String(t(e.widget.bot_messages)),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"})),c.a.createElement(M.a,{className:"text-16",color:"textSecondary"},"\ucd1d \uc0ac\uc6a9\uc790 \uba54\uc2dc\uc9c0 \uac74\uc218 / \ucc57\ubd07 \uba54\uc2dc\uc9c0 \uac74\uc218")))}),T=a(305),_=a.n(T);var I=c.a.memo(function(e){var t,a=e.widget,n=_.a.sumBy(a,"n_user_messages");return c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"p-16 pr-4 flex flex-row items-center"},c.a.createElement(k.a,{className:"mr-12"},"chat"),c.a.createElement(M.a,{className:"h3 font-bold"},"\uc0ac\uc6a9\uc790 \uba54\uc2dc\uc9c0 \ud604\ud669")),c.a.createElement("div",{className:"text-center pt-12 pb-28"},c.a.createElement(M.a,{component:"div",className:"text-48 leading-none text-red"},c.a.createElement(A.Random,{text:String((t=n,String(t).replace(/(\d)(?=(?:\d{3})+(?!\d))/g,"$1,"))),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"})),c.a.createElement(M.a,{className:"text-16",color:"textSecondary"},"\uc0ac\uc6a9\uc790 \uba54\uc2dc\uc9c0 \uac74\uc218")))});var B=c.a.memo(function(e){return c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"p-16 pr-4 flex flex-row items-center"},c.a.createElement(k.a,{className:"mr-12"},"chat"),c.a.createElement(M.a,{className:"h3 font-bold"},"\ub300\ud654 \ud604\ud669")),c.a.createElement("div",{className:"text-center pt-12 pb-28"},c.a.createElement(M.a,{component:"div",className:"text-48 leading-none text-orange"},c.a.createElement(A.Random,{text:String((t=e.widget.length,String(t).replace(/(\d)(?=(?:\d{3})+(?!\d))/g,"$1,"))),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"})),c.a.createElement(M.a,{className:"text-16",color:"textSecondary"},"\ucd1d \ub300\ud654 \uac74\uc218")));var t});var H=c.a.memo(function(e){var t=e.widget,a=0,n=0;function r(e){return String(e).replace(/(\d)(?=(?:\d{3})+(?!\d))/g,"$1,")}return _.a.forEach(t,function(e,t){_.a.filter(e.actions,function(e){"action_default_fallback"===e&&a++,"action_help"===e&&n++})}),c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"p-16 pr-4 flex flex-row items-center"},c.a.createElement(k.a,{className:"mr-12"},"chat"),c.a.createElement(M.a,{className:"h3 font-bold"},"\ub300\ud654 \uc0c1\uc138 \ud604\ud669")),c.a.createElement("div",{className:"text-center pt-12 pb-28"},c.a.createElement(M.a,{component:"div",className:"text-48 leading-none text-green  inline-flex"},c.a.createElement(A.Random,{text:String(r(a)),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"}),"\xa0/\xa0",c.a.createElement(A.Random,{text:String(r(n)),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"})),c.a.createElement(M.a,{className:"text-16",color:"textSecondary"},"fallback \ub300\ud654 \uac74\uc218 / \ub3c4\uc6c0\ub9d0 \ub300\ud654 \uac74\uc218")))}),R=a(893),V=a(999),F=a(290);function L(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),a.push.apply(a,n)}return a}var $=c.a.memo(function(e){var t={},a={firstView:"\ucd5c\uadfc 10\uc77c\uac04 \ud604\ud669",secondView:"\ucd5c\uadfc 1\uac1c\uc6d4\uac04 \ud604\ud669"},i=Object(l.useState)("firstView"),o=Object(r.a)(i,2),s=o[0],d=o[1],m=Object(l.useState)(!0),f=Object(r.a)(m,2),u=f[0],p=f[1];function b(e){d(e)}function g(e){return String(e).replace(/(\d)(?=(?:\d{3})+(?!\d))/g,"$1,")}Object(l.useEffect)(function(){p(!0),setTimeout(function(){p(!1)},1e3)},[e]);var x={},y=[],E=0,w=0,h=0,v=0;if(null!==e.widget){_.a.forEach(e.widget[s],function(e,t){E=0,w=0,h=0,v=0;var a=N.a.unix(e.latest_event_time).format("YYYY-MM-DD");_.a.filter(e.actions,function(e){"action_default_fallback"===e&&(w=1),"action_help"===e&&(h=1)}),E=1,v=e.n_user_messages,y.push({dateString:a,userMessageCnt:v,totalCnt:E,fallbackCnt:w,helpCnt:h})});var O=_()(y).groupBy("dateString").map(function(e,t){return{dateString:t,userMessageCnt:_.a.sumBy(e,"userMessageCnt"),totalCnt:_.a.sumBy(e,"totalCnt"),fallbackCnt:_.a.sumBy(e,"fallbackCnt"),helpCnt:_.a.sumBy(e,"helpCnt")}}).value(),D=_.a.orderBy(O,["dateString"],["asc"]),j=[];null!==(x=function(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?L(a,!0).forEach(function(t){Object(n.a)(e,t,a[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):L(a).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))})}return e}({},x,Object(n.a)({},s,{labels:_.a.map(D,"dateString"),datasets:[{type:"line",label:"\uc0ac\uc6a9\uc790 \uba54\uc2dc\uc9c0 \uac74\uc218",data:_.a.map(D,"userMessageCnt"),backgroundColor:"#ffd43b",borderColor:"#ffd43b",fill:!1,yAxisID:"y-axis-2"},{type:"bar",label:"\ucd1d \ub300\ud654 \uac74\uc218",data:_.a.map(D,"totalCnt"),backgroundColor:"#0b7285",hoverBackgroundColor:"#0c8599",yAxisID:"y-axis-1"},{type:"bar",label:"fallback \ub300\ud654 \uac74\uc218",data:_.a.map(D,"fallbackCnt"),backgroundColor:"#15aabf",hoverBackgroundColor:"#22b8cf",yAxisID:"y-axis-1"},{type:"bar",label:"\ub3c4\uc6c0\ub9d0 \ub300\ud654 \uac74\uc218",data:_.a.map(D,"helpCnt"),backgroundColor:"#66d9e8",hoverBackgroundColor:"#99e9f2",yAxisID:"y-axis-1"}]})))[s]&&(j=(j=x[s].labels).map(function(e){return N()(e).format("MM-DD")})),t={responsive:!0,maintainAspectRatio:!1,legend:{display:!0,position:"bottom",labels:{fontColor:"white"}},tooltips:{mode:"label",callbacks:{label:function(e,t){var a=t.datasets[e.datasetIndex].label||"";return a&&(a+=": "),a+=g(e.yLabel),a}}},scales:{xAxes:[{stacked:!0,display:!0,gridLines:{display:!0,color:"#5D5D5D"},ticks:{beginAtZero:!0,fontColor:"white"},labels:j}],yAxes:[{id:"y-axis-1",stacked:!0,type:"linear",display:!0,position:"left",gridLines:{display:!0,color:"#5D5D5D"},ticks:{fontColor:"#66d9e8",callback:function(e,t,a){return g(e)}},labels:{show:!0}},{id:"y-axis-2",stacked:!0,type:"linear",display:!0,position:"right",gridLines:{display:!0},ticks:{fontColor:"#ffd43b",callback:function(e,t,a){return g(e)}},labels:{show:!0}}]}}}return null===e.widget||null===e.widget[s]||0===e.widget[s].length?c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"flex items-center justify-between px-16 py-16 border-b-1"},c.a.createElement(M.a,{className:"h3 font-bold"},"\uc77c\ubcc4 \uba54\uc2dc\uc9c0 \ubc0f \ub300\ud654 \ud604\ud669"),c.a.createElement("div",{className:"items-center"},Object.entries(a).map(function(e){var t=Object(r.a)(e,2),a=t[0],n=t[1];return c.a.createElement(R.a,{key:a,className:"normal-case shadow-none px-16",onClick:function(){return b(a)},color:s===a?"secondary":"default",variant:s===a?"contained":"text"},n)}))),c.a.createElement("div",{className:"flex flex-row flex-wrap"},c.a.createElement("div",{className:"w-full p-8 min-h-420 h-420",style:{minHeight:"306px"}},u&&c.a.createElement("div",{style:{width:"100%",height:"290px",textAlign:"center",padding:"20px"}},c.a.createElement(V.a,{color:"secondary",style:{display:"inline-block"}})),!u&&c.a.createElement(M.a,{className:"text-center text-white text-13",style:{paddingTop:"130px"}},"\uc870\ud68c\ub0b4\uc5ed\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.")))):c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"flex items-center justify-between px-16 py-16 border-b-1"},c.a.createElement("div",{className:"items-center flex"},c.a.createElement(k.a,{className:"mr-12"},"insert_chart_outlined"),c.a.createElement(M.a,{className:"h3 font-bold"},"\uc77c\ubcc4 \uba54\uc2dc\uc9c0 & \ub300\ud654 \ud604\ud669 ( "+x[s].labels[0]+" ~ "+x[s].labels[x[s].labels.length-1]+" )")),c.a.createElement("div",{className:"items-center"},Object.entries(a).map(function(e){var t=Object(r.a)(e,2),a=t[0],n=t[1];return c.a.createElement(R.a,{key:a,className:"normal-case shadow-none px-16",onClick:function(){return b(a)},color:s===a?"secondary":"default",variant:s===a?"contained":"text"},n)}))),c.a.createElement("div",{className:"flex flex-row flex-wrap"},c.a.createElement("div",{className:"w-full p-8 min-h-420 h-420",style:{minHeight:"306px"}},u&&c.a.createElement("div",{style:{width:"100%",height:"290px",textAlign:"center",padding:"20px"}},c.a.createElement(V.a,{color:"secondary",style:{display:"inline-block"}})),!u&&c.a.createElement(F.a,{data:{labels:x[s].labels,datasets:x[s].datasets},width:800,height:290,options:t}))))});var G=c.a.memo(function(e){var t=e.widget,a=Object(l.useState)(!0),n=Object(r.a)(a,2),i=n[0],o=n[1];Object(l.useEffect)(function(){o(!0),setTimeout(function(){o(!1)},1e3)},[e]);var s=[];_.a.forEach(t,function(e){_.a.forEach(e.intents,function(e){"get_started"!==e&&"\ud658\uc601\uc778\uc0ac"!==e&&"\uc791\ubcc4\uc778\uc0ac"!==e&&s.push({intent:e})})});var d=_.a.map(_.a.countBy(s,"intent"),function(e,t){return{intent:t,cnt:e}}),m=_.a.orderBy(d,["cnt"],["desc"]);return m=m.filter(function(e,t){return t>=0&&t<=4}),c.a.createElement(S.a,{className:"w-full rounded-8 shadow-none border-1"},c.a.createElement("div",{className:"p-16 pr-4 flex flex-row items-center"},c.a.createElement(k.a,{className:"mr-12"},"format_list_numbered"),c.a.createElement(M.a,{className:"h3 font-bold"},"\uc778\ud150\ud2b8 \uc0c1\uc704 Top 5")),i&&c.a.createElement("div",{style:{width:"100%",textAlign:"center",padding:"20px"}},c.a.createElement(V.a,{color:"secondary",style:{display:"inline-block"}})),!i&&c.a.createElement("table",{className:"simple"},c.a.createElement("thead",null,c.a.createElement("tr",null,c.a.createElement("th",{className:"text-center"},"\uc778\ud150\ud2b8"),c.a.createElement("th",{className:"text-center"},"\ub300\ud654 \uac74\uc218"))),c.a.createElement("tbody",null,m&&0===m.length&&c.a.createElement("tr",null,c.a.createElement("td",{colSpan:"2"},c.a.createElement(M.a,{className:"text-center text-white text-13"},"\uc870\ud68c\ub0b4\uc5ed\uc774 \uc5c6\uc2b5\ub2c8\ub2e4."))),m&&m.map(function(e,t){return c.a.createElement("tr",{key:t},c.a.createElement("td",{className:0===t?"text-red-400 font-bold text-13":1===t?"text-blue-400 font-bold text-13":2===t?"text-green-400 font-bold text-13":"text-white text-13",title:e.intent},c.a.createElement(A.Random,{text:(n=e.intent,r=14,l="...",""!==r&&null!=r||(r=20),""!==l&&null!=l||(l="..."),n.length>r&&(n=n.substr(0,r)+l),n),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"})),c.a.createElement("td",{className:0===t?"text-red-400 font-bold text-13 text-right":1===t?"text-blue-400 font-bold text-13 text-right":2===t?"text-green-400 font-bold text-13 text-right":"text-white text-13 text-right"},c.a.createElement(A.Random,{text:(a=e.cnt,String(a).replace(/(\d)(?=(?:\d{3})+(?!\d))/g,"$1,")+"\uac74"),iterations:1,effect:"verticalFadeIn",effectChange:2,effectDirection:"down"})));var a,n,r,l}))))}),J=(a(1187),a(896)),U=a(462),K=a(897),Z=a(1189),q=a.n(Z),z=a(1006),Q=a(1188),W=a.n(Q),X=a(1199),ee=a(871),te=a(1260),ae=a(1200);function ne(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),a.push.apply(a,n)}return a}var re=Object(z.a)(function(e){return{content:{"& canvas":{maxHeight:"100%"}}}});t.default=Object(o.a)("dashboardApp",O)(function(e){var t=Object(i.b)(),a=Object(i.c)(function(e){return e.dashboardApp.dashboard.conversations}),o=Object(i.c)(function(e){return e.dashboardApp.dashboard.conversationsChart}),s=Object(i.c)(function(e){return e.dashboardApp.dashboard.statistics}),f=re(e),u=Object(l.useRef)(null),x=Object(l.useState)({dateString:N()().format(N.a.HTML5_FMT.DATE),start:N()(N()().format(N.a.HTML5_FMT.DATE),"YYYY.MM.DD").unix(),until:N()(N()().add(1,"day").format("YYYY.MM.DD"),"YYYY.MM.DD").unix()}),y=Object(r.a)(x,2),E=y[0],w=y[1],h=Object(l.useState)(N()().format("YYYY-MM-DD HH:mm:ss")),v=Object(r.a)(h,2),O=v[0],D=v[1];Object(l.useEffect)(function(){S(E)},[]),Object(j.a)(function(){S(E)},3e5);var S=function(e){if(void 0!==e){t(function(){var e=d.a.get("/api/statistics");return function(t){return e.then(function(e){return t({type:p,payload:e.data})})}}()),t(function(e){var t="";t=void 0!==e?"offset=0&intent=&entity=&action=&policies=&exclude_self=true&"+Object.keys(e).map(function(t){return t+"="+e[t]}).join("&"):"offset=0&intent=&entity=&action=&policies=&exclude_self=true";var a=d.a.get(b+"?"+t);return function(e){return a.then(function(t){e({type:m,payload:t.data})})}}({start:e.start,until:e.until}));var a=N()(e.dateString).subtract(10,"day").format("YYYY-MM-DD"),n=N()(a,"YYYY.MM.DD").unix();t(g("firstView",{start:n,until:e.until}));var r=N()(e.dateString).subtract(1,"month").format("YYYY-MM-DD"),l=N()(r,"YYYY.MM.DD").unix();t(g("secondView",{start:l,until:e.until})),D(N()().format("YYYY-MM-DD HH:mm:ss"))}};return a&&s?c.a.createElement(Y.o,{classes:{header:"min-h-130 h-130",content:f.content},header:c.a.createElement("div",{className:"flex flex-col justify-between flex-1 px-24"},c.a.createElement("div",{className:"flex items-center flex-1"},c.a.createElement(Y.c,{animation:"transition.expandIn",delay:300},c.a.createElement(k.a,{className:"text-32 mr-16"},"dashboard")),c.a.createElement(Y.c,{animation:"transition.slideLeftIn",delay:300},c.a.createElement("span",{className:"text-24"},"Dashboard"))),c.a.createElement("div",{className:"flex justify-between items-end"},c.a.createElement(J.a,{lgUp:!0},c.a.createElement(U.a,{"aria-label":"open left sidebar"},c.a.createElement(k.a,null,"menu"))))),content:c.a.createElement("div",{className:"p-12"},c.a.createElement("div",{className:"widget flex w-full px-12"},c.a.createElement("div",{className:"flex items-center justify-between"},c.a.createElement(ee.a,{utils:X.a,locale:ae.a},c.a.createElement(te.a,{style:{width:"160px"},autoOk:!0,disableFuture:!0,variant:"inline",color:"secondary",inputVariant:"outlined",format:"yyyy-MM-dd",margin:"normal",id:"date-picker-inline",label:"\uc870\ud68c\uc77c\uc790",value:E.dateString,onChange:function(e){var t=N()(e,"YYYY.MM.DD").unix(),a=N()(e).add(1,"day").format("YYYY.MM.DD");w(function(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?ne(a,!0).forEach(function(t){Object(n.a)(e,t,a[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):ne(a).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))})}return e}({},E,{dateString:N()(e).format(N.a.HTML5_FMT.DATE),start:t,until:N()(a,"YYYY.MM.DD").unix()})),S({dateString:N()(e).format(N.a.HTML5_FMT.DATE),start:t,until:N()(a,"YYYY.MM.DD").unix()})},KeyboardButtonProps:{"aria-label":"change date",style:{padding:0}},InputAdornmentProps:{position:"start"}})),c.a.createElement(M.a,{variant:"subtitle2",className:"pl-5 py-0 sm:py-24"},"\uc870\ud68c\uc2dc\uac04 : ",O,c.a.createElement(R.a,{variant:"contained",color:"secondary",className:Object(C.a)("sm:ml-12",f.button),startIcon:c.a.createElement(W.a,null),onClick:function(){return S(E)}},"\uc870\ud68c")),c.a.createElement(K.a,{variant:"outlined",color:"secondary",label:"\ub370\uc774\ud130\ub294 5\ubd84\ub9c8\ub2e4 \uc790\ub3d9 \uac31\uc2e0 \ub429\ub2c8\ub2e4.",icon:c.a.createElement(q.a,null),className:"ml-12"}))),c.a.createElement(Y.d,{className:"flex flex-wrap",enter:{animation:"transition.slideUpBigIn"}},c.a.createElement("div",{className:"widget flex w-full sm:w-1/2 md:w-1/4 p-12"},c.a.createElement(P,{widget:s})),c.a.createElement("div",{className:"widget flex w-full sm:w-1/2 md:w-1/4 p-12"},c.a.createElement(I,{widget:a,date:E.dateString})),c.a.createElement("div",{className:"widget flex w-full sm:w-1/2 md:w-1/4 p-12"},c.a.createElement(B,{widget:a,date:E.dateString})),c.a.createElement("div",{className:"widget flex w-full sm:w-1/2 md:w-1/4 p-12"},c.a.createElement(H,{widget:a,date:E.dateString})),c.a.createElement("div",{className:"widget flex w-full sm:w-1/2 md:w-3/4 p-12"},c.a.createElement($,{widget:o,date:E.dateString})),c.a.createElement("div",{className:"widget flex w-full sm:w-1/2 md:w-1/4 p-12"},c.a.createElement(G,{widget:a,date:E.dateString})))),ref:u}):null})}}]);