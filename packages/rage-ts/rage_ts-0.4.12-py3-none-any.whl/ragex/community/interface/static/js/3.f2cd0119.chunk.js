(this["webpackJsonpucess-talk-admin"]=this["webpackJsonpucess-talk-admin"]||[]).push([[3],{951:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"Timeline",{enumerable:!0,get:function(){return o.default}}),Object.defineProperty(t,"TimelineEvent",{enumerable:!0,get:function(){return r.default}}),Object.defineProperty(t,"TimelineBlip",{enumerable:!0,get:function(){return l.default}});var o=i(n(987)),r=i(n(988)),l=i(n(989));function i(e){return e&&e.__esModule?e:{default:e}}},952:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var o={container:{position:"relative",fontSize:"80%",fontWeight:300,padding:"10px 0",width:"95%",margin:"0 auto"},containerBefore:{content:"",position:"absolute",top:0,height:"100%",width:2,background:"#a0b2b8"},"containerBefore--left":{left:"16px"},"containerBefore--right":{right:"14px"},containerAfter:{content:"",display:"table",clear:"both"},event:{position:"relative",margin:"10px 0"},"event--left":{paddingLeft:45,textAlign:"left"},"event--right":{paddingRight:45,textAlign:"right"},eventAfter:{clear:"both",content:"",display:"table"},eventType:{position:"absolute",top:0,borderRadius:"50%",width:30,height:30,marginLeft:1,background:"#e9f0f5",border:"2px solid #6fba1c",display:"flex"},"eventType--left":{left:0},"eventType--right":{right:0},materialIcons:{display:"flex",width:32,height:32,position:"relative",justifyContent:"center",cursor:"pointer",alignSelf:"center",alignItems:"center"},eventContainer:{position:"relative"},eventContainerBefore:{top:24,left:"100%",borderColor:"transparent",borderLeftColor:"#ffffff"},time:{marginBottom:3},subtitle:{marginTop:2,fontSize:"85%",color:"#777"},message:{width:"98%",backgroundColor:"#ffffff",boxShadow:"0 1px 3px 0 rgba(0, 0, 0, 0.1)",marginTop:"1em",marginBottom:"1em",lineHeight:1.6,padding:"0.5em 1em"},messageAfter:{clear:"both",content:"",display:"table"},actionButtons:{marginTop:-20},"actionButtons--left":{float:"left",textAlign:"left"},"actionButtons--right":{float:"right",textAlign:"right"},card:{boxShadow:"rgba(0, 0, 0, 0.117647) 0px 1px 6px, rgba(0, 0, 0, 0.117647) 0px 1px 4px",backgroundColor:"rgb(255, 255, 255)"},cardTitle:{backgroundColor:"#7BB1EA",padding:10,color:"#fff"},cardBody:{backgroundColor:"#ffffff",marginBottom:"1em",lineHeight:1.6,padding:10,minHeight:40},blipStyle:{position:"absolute",top:"50%",marginTop:"9px"},toggleEnabled:{cursor:"pointer"}};t.default=o},953:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o,r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e},l="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i=function(){function e(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}return function(t,n,o){return n&&e(t.prototype,n),o&&e(t,o),t}}(),a=n(0),u=(o=a)&&o.__esModule?o:{default:o};var c={breakpointCols:void 0,className:void 0,columnClassName:void 0,children:void 0,columnAttrs:void 0,column:void 0},f=2,s=function(e){function t(e){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t);var n=function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!==typeof t&&"function"!==typeof t?e:t}(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,e));n.reCalculateColumnCount=n.reCalculateColumnCount.bind(n),n.reCalculateColumnCountDebounce=n.reCalculateColumnCountDebounce.bind(n);var o=void 0;return o=n.props.breakpointCols&&n.props.breakpointCols.default?n.props.breakpointCols.default:parseInt(n.props.breakpointCols)||f,n.state={columnCount:o},n}return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,u.default.Component),i(t,[{key:"componentDidMount",value:function(){this.reCalculateColumnCount(),window&&window.addEventListener("resize",this.reCalculateColumnCountDebounce)}},{key:"componentDidUpdate",value:function(){this.reCalculateColumnCount()}},{key:"componentWillUnmount",value:function(){window&&window.removeEventListener("resize",this.reCalculateColumnCountDebounce)}},{key:"reCalculateColumnCountDebounce",value:function(){var e=this;window&&window.requestAnimationFrame?(window.cancelAnimationFrame&&window.cancelAnimationFrame(this._lastRecalculateAnimationFrame),this._lastRecalculateAnimationFrame=window.requestAnimationFrame(function(){e.reCalculateColumnCount()})):this.reCalculateColumnCount()}},{key:"reCalculateColumnCount",value:function(){var e=window&&window.innerWidth||1/0,t=this.props.breakpointCols;"object"!==("undefined"===typeof t?"undefined":l(t))&&(t={default:parseInt(t)||f});var n=1/0,o=t.default||f;for(var r in t){var i=parseInt(r);i>0&&e<=i&&i<n&&(n=i,o=t[r])}o=Math.max(1,parseInt(o)||1),this.state.columnCount!==o&&this.setState({columnCount:o})}},{key:"itemsInColumns",value:function(){for(var e=this.state.columnCount,t=new Array(e),n=[].concat(this.props.children||[]),o=0;o<n.length;o++){var r=o%e;t[r]||(t[r]=[]),t[r].push(n[o])}return t}},{key:"renderColumns",value:function(){var e=this.props,t=e.column,n=e.columnAttrs,o=void 0===n?{}:n,l=e.columnClassName,i=this.itemsInColumns(),a=100/i.length+"%",c=l;"string"!==typeof c&&(this.logDeprecated('The property "columnClassName" requires a string'),"undefined"===typeof c&&(c="my-masonry-grid_column"));var f=r({},t,o,{style:r({},o.style,{width:a}),className:c});return i.map(function(e,t){return u.default.createElement("div",r({},f,{key:t}),e)})}},{key:"logDeprecated",value:function(e){console.error("[Masonry]",e)}},{key:"render",value:function(){var e=this.props,t=(e.children,e.breakpointCols,e.columnClassName,e.columnAttrs,e.column,e.className),n=function(e,t){var n={};for(var o in e)t.indexOf(o)>=0||Object.prototype.hasOwnProperty.call(e,o)&&(n[o]=e[o]);return n}(e,["children","breakpointCols","columnClassName","columnAttrs","column","className"]),o=t;return"string"!==typeof t&&(this.logDeprecated('The property "className" requires a string'),"undefined"===typeof t&&(o="my-masonry-grid")),u.default.createElement("div",r({},n,{className:o}),this.renderColumns())}}]),t}();s.defaultProps=c,t.default=s},987:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var o=function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var n in e)if(Object.prototype.hasOwnProperty.call(e,n)){var o=Object.defineProperty&&Object.getOwnPropertyDescriptor?Object.getOwnPropertyDescriptor(e,n):{};o.get||o.set?Object.defineProperty(t,n,o):t[n]=e[n]}return t.default=e,t}(n(0)),r=i(n(2)),l=i(n(952));function i(e){return e&&e.__esModule?e:{default:e}}function a(e){return(a="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function u(){return(u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e}).apply(this,arguments)}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{},o=Object.keys(n);"function"===typeof Object.getOwnPropertySymbols&&(o=o.concat(Object.getOwnPropertySymbols(n).filter(function(e){return Object.getOwnPropertyDescriptor(n,e).enumerable}))),o.forEach(function(t){f(e,t,n[t])})}return e}function f(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},l=Object.keys(e);for(o=0;o<l.length;o++)n=l[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(o=0;o<l.length;o++)n=l[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}function p(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function d(e,t){return!t||"object"!==a(t)&&"function"!==typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function b(e,t){return(b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}var m=function(e){function t(){return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),d(this,y(t).apply(this,arguments))}var n,r,i;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(t,o.Component),n=t,(r=[{key:"render",value:function(){var e=this.props,t=e.orientation,n=void 0===t?"left":t,r=e.children,i=e.lineColor,a=e.lineStyle,f=e.style,p=s(e,["orientation","children","lineColor","lineStyle","style"]),d=o.default.Children.map(r,function(e){return o.default.cloneElement(e,{orientation:n})}),y=c({},"right"===n?l.default["containerBefore--right"]:l.default["containerBefore--left"]),b=c({},y,a);return b=i?c({},b,{background:i}):b,o.default.createElement("div",null,o.default.createElement("section",u({style:c({},l.default.container,f)},p),o.default.createElement("div",{style:c({},l.default.containerBefore,b)}),d,o.default.createElement("div",{style:l.default.containerAfter})))}}])&&p(n.prototype,r),i&&p(n,i),t}();m.propTypes={children:r.default.node.isRequired,orientation:r.default.string,style:r.default.object,lineColor:r.default.string,lineStyle:r.default.object},m.defaultProps={style:{},lineStyle:{}};var h=m;t.default=h},988:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var o=i(n(2)),r=function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var n in e)if(Object.prototype.hasOwnProperty.call(e,n)){var o=Object.defineProperty&&Object.getOwnPropertyDescriptor?Object.getOwnPropertyDescriptor(e,n):{};o.get||o.set?Object.defineProperty(t,n,o):t[n]=e[n]}return t.default=e,t}(n(0)),l=i(n(952));function i(e){return e&&e.__esModule?e:{default:e}}function a(e){return(a="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function u(){return(u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e}).apply(this,arguments)}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{},o=Object.keys(n);"function"===typeof Object.getOwnPropertySymbols&&(o=o.concat(Object.getOwnPropertySymbols(n).filter(function(e){return Object.getOwnPropertyDescriptor(n,e).enumerable}))),o.forEach(function(t){f(e,t,n[t])})}return e}function f(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function d(e,t){return(d=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function y(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}var b=function(e){function t(e){var n,o,r;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),o=this,(n=!(r=p(t).call(this,e))||"object"!==a(r)&&"function"!==typeof r?y(o):r).state={showContent:n.props.showContent},n.toggleContent=n.toggleContent.bind(y(y(n))),n}var n,o,i;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&d(e,t)}(t,r.Component),n=t,(o=[{key:"componentDidUpdate",value:function(e){this.props.showContent!==e.showContent&&this.state({showContent:this.props.showContent})}},{key:"mergeNotificationStyle",value:function(e,t,n){var o=e?c({},l.default.eventType,{color:e,borderColor:e}):l.default.eventType,r=c({},"right"===n?l.default["eventType--right"]:l.default["eventType--left"]);return c({},o,r,t)}},{key:"mergeContentStyle",value:function(e){var t=this.showAsCard()?l.default.cardBody:l.default.message;return e?c({},t,e):t}},{key:"timeStyle",value:function(){return this.showAsCard()?l.default.time:c({},l.default.time,{color:"#303e49"})}},{key:"showAsCard",value:function(){return"card"===this.props.container}},{key:"containerStyle",value:function(){var e=this.props.style,t=c({},l.default.eventContainer,e);return this.showAsCard()?c({},l.default.card,t):t}},{key:"toggleStyle",value:function(){var e=this.props,t=e.container,n=e.cardHeaderStyle,o=e.collapsible,r="card"===t?c({},l.default.cardTitle,n):{};return o?c({},l.default.toggleEnabled,r):r}},{key:"toggleContent",value:function(){this.setState({showContent:!this.state.showContent})}},{key:"renderChildren",value:function(){var e=this.props,t=e.collapsible,n=e.contentStyle;return t&&this.state.showContent||!t?r.default.createElement("div",{style:this.mergeContentStyle(n)},this.props.children,r.default.createElement("div",{style:l.default.messageAfter})):r.default.createElement("span",{style:{fontWeight:500,fontSize:16,cursor:"pointer"},onClick:this.toggleContent},"\u2026")}},{key:"render",value:function(){var e=this.props,t=e.createdAt,n=e.title,o=e.subtitle,i=e.iconStyle,a=e.bubbleStyle,f=e.buttons,s=e.icon,p=e.iconColor,d=e.titleStyle,y=e.subtitleStyle,b=e.orientation,m=e.collapsible,h=e.onClick,v=e.onIconClick,g=e.className,O=c({},"right"===b?l.default["event--right"]:l.default["event--left"]),C=c({},"left"===b?l.default["actionButtons--right"]:l.default["actionButtons--left"]);return r.default.createElement("div",{style:c({},l.default.event,O)},r.default.createElement("div",{style:this.mergeNotificationStyle(p,a,b)},r.default.createElement("span",{style:c({},l.default.materialIcons,i),onClick:v},s)),r.default.createElement("div",u({style:this.containerStyle()},{onClick:h,className:g}),r.default.createElement("div",{style:l.default.eventContainerBefore}),r.default.createElement("div",{style:this.toggleStyle(),onClick:m&&this.toggleContent},t&&r.default.createElement("div",{style:this.timeStyle()},t),r.default.createElement("div",{style:d},n),o&&r.default.createElement("div",{style:c({},l.default.subtitle,y)},o),r.default.createElement("div",{style:c({},l.default.actionButtons,C)},f)),this.props.children&&this.renderChildren()),r.default.createElement("div",{style:l.default.eventAfter}))}}])&&s(n.prototype,o),i&&s(n,i),t}();b.propTypes={title:o.default.node.isRequired,subtitle:o.default.node,createdAt:o.default.node,children:o.default.node,buttons:o.default.node,container:o.default.string,icon:o.default.node,iconColor:o.default.string,iconStyle:o.default.object,bubbleStyle:o.default.object,orientation:o.default.string,contentStyle:o.default.object,cardHeaderStyle:o.default.object,style:o.default.object,titleStyle:o.default.object,subtitleStyle:o.default.object,collapsible:o.default.bool,showContent:o.default.bool,className:o.default.string,onClick:o.default.func,onIconClick:o.default.func},b.defaultProps={createdAt:void 0,iconStyle:{},bubbleStyle:{},contentStyle:{},cardHeaderStyle:{},style:{},titleStyle:{},subtitleStyle:{},orientation:"left",showContent:!1,className:"",onClick:function(){},onIconClick:function(){}};var m=b;t.default=m},989:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var o=function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var n in e)if(Object.prototype.hasOwnProperty.call(e,n)){var o=Object.defineProperty&&Object.getOwnPropertyDescriptor?Object.getOwnPropertyDescriptor(e,n):{};o.get||o.set?Object.defineProperty(t,n,o):t[n]=e[n]}return t.default=e,t}(n(0)),r=i(n(2)),l=i(n(952));function i(e){return e&&e.__esModule?e:{default:e}}function a(e){return(a="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function u(){return(u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e}).apply(this,arguments)}function c(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},l=Object.keys(e);for(o=0;o<l.length;o++)n=l[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(o=0;o<l.length;o++)n=l[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}function f(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{},o=Object.keys(n);"function"===typeof Object.getOwnPropertySymbols&&(o=o.concat(Object.getOwnPropertySymbols(n).filter(function(e){return Object.getOwnPropertyDescriptor(n,e).enumerable}))),o.forEach(function(t){s(e,t,n[t])})}return e}function s(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function p(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function d(e,t){return!t||"object"!==a(t)&&"function"!==typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function b(e,t){return(b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}var m=function(e){function t(){return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),d(this,y(t).apply(this,arguments))}var n,r,i;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(t,o.Component),n=t,(r=[{key:"mergeNotificationStyle",value:function(e){return e?f({},l.default.eventType,{color:e,borderColor:e}):l.default.eventType}},{key:"iconStyle",value:function(e){return f({},l.default.materialIcons,e)}},{key:"render",value:function(){var e=this.props,t=e.title,n=e.iconStyle,r=e.icon,i=e.orientation,a=e.iconColor,s=e.style,p=c(e,["title","iconStyle","icon","orientation","iconColor","style"]),d=f({},"right"===i?l.default["event--right"]:l.default["event--left"]);return o.default.createElement("div",{style:f({},l.default.event,{marginBottom:50},s)},o.default.createElement("div",{style:this.mergeNotificationStyle(a)},o.default.createElement("span",{style:this.iconStyle(n)},r)),o.default.createElement("div",u({},p,{style:f({},l.default.blipStyle,d)}),o.default.createElement("div",null,t)),o.default.createElement("div",{style:l.default.eventAfter}))}}])&&p(n.prototype,r),i&&p(n,i),t}();m.propTypes={title:r.default.node.isRequired,icon:r.default.node,iconColor:r.default.string,iconStyle:r.default.object,style:r.default.object,orientation:r.default.string},m.defaultProps={iconStyle:{},style:{}};var h=m;t.default=h}}]);