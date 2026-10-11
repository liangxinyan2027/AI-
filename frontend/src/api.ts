export const STATIC_MODE = import.meta.env.VITE_PORTFOLIO_MODE === 'true';
export const assetUrl = (path:string) => import.meta.env.BASE_URL + path;
export const downloadUrl = (kind:string) => STATIC_MODE ? assetUrl('demo/'+({data:'campaign.csv',predictions:'predictions.csv',report:'validation_report.json'}[kind])) : '/api/download/'+kind;
let snapshot:Promise<any>|undefined;
function demo(){return snapshot ||= fetch(assetUrl('demo/snapshot.json')).then(r=>{if(!r.ok)throw new Error('展示数据加载失败');return r.json()}).catch(e=>{snapshot=undefined;throw e});}
export async function api(path:string, options?:RequestInit) {
 if(STATIC_MODE){
  if(options?.method && options.method!=='GET')throw new Error('作品集展示版不支持上传和重新训练。');
  const d=await demo();const url=new URL(path,'https://demo.local');
  switch(url.pathname){
   case '/health':return {status:'ready',error:null,dataset:d.summary.name};
   case '/dataset/summary':return d.summary;
   case '/data-quality':return d.quality;
   case '/model/summary':case '/model/validation':return d.model;
   case '/model/segments':return d.model.report.groups;
   case '/model/predictions':{
    const group=url.searchParams.get('group'),search=url.searchParams.get('search')||'';
    const page=Math.max(1,Number(url.searchParams.get('page'))||1);
    const rows=d.predictions.filter((r:any)=>(!group||r.response_group===group)&&String(r.user_id).includes(search));
    return {rows:rows.slice((page-1)*30,page*30),total:rows.length,groups:d.groups};
   }
   default:throw new Error('展示版中没有此数据接口');
  }
 }
  const response = await fetch('/api'+path,options);
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail==='string'?data.detail:'请求失败，请重试。');
  return data;
}
