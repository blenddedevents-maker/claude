const {chromium}=require('playwright');
(async()=>{
  const [,,html,out,vs]=process.argv; const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  for(const v of vs.split(',')){
    await p.goto('file://'+html+'?v='+v); await p.waitForSelector('body[data-ready]'); await p.waitForTimeout(300);
    await p.locator('#poster').screenshot({path:out.replace('%',v)});
  }
  await b.close();
})();
