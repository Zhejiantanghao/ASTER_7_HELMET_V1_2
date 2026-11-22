# ASTER-7 设计档案网页框架

直接打开 `dist/index.html` 可查看；也可在 dist 下启动静态服务器。内容在 `dist/content.js`，样式在 `dist/style.css`，交互在 `dist/app.js`。

目前 01、02、03 三方向各有三个占位案例，均为展示结构，不代表真实完成数量。参考图、案例图均未填充；验收状态全部待测。

后续填充：图片放入 dist/assets，再将 content.js 中对应 image 字段从 null 改为 assets/文件名。每个案例 references 固定五条，分别填写 source、url、learn、application。prompt 填实际提示词；logs 填 {date,title,text}。案例可增删。主题与三根支柱取自当前 BASE_ART.md，本框架保留其快照；MD 更新后同步 content.js。

图像原件继续保存在研究目录，不覆盖；网页使用副本。首页参考主视觉暂为占位。

导航已改为点击式四层页面：首页 → 方向选择 → 方向案例 → 案例详情；每页有返回入口，URL hash 路由支持浏览器前进后退及直接访问。案例详情不再弹窗。
