import {useState} from 'react';
import {motion,useReducedMotion} from 'framer-motion';
import {ArrowRightCircle} from 'lucide-react';
const VIDEO='https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260518_003132_8b7edcb6-c64d-4a52-a9ca-879942e122ad.mp4';
export function Logo(){return <svg role="img" aria-label="AI 广告增长优化助手" width="32" height="32" viewBox="0 0 256 256"><path d="M 64 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 L 128 64 L 128 64.5 L 161 32 L 192 0 L 256 0 L 256 64 L 192 128 L 128 128 L 128 192 L 96 223 L 63.5 256 L 0 256 L 0 192 Z M 256 192 L 224 223 L 191.5 256 L 128 256 L 128 192 L 192 128 L 256 128 Z" fill="currentColor"/></svg>}
export function Hero(){
 const reduced=useReducedMotion(); const [failed,setFailed]=useState(false);
 const fade=(i:number)=>({initial:{opacity:0,y:reduced?0:28},animate:{opacity:1,y:0},transition:{delay:reduced?0:i*.15,duration:reduced?0:.6,ease:[.22,1,.36,1] as [number,number,number,number]}});
 return <section className="hero" aria-label="产品首页">
  {!failed&&!reduced&&<video className="hero-video" autoPlay muted loop playsInline onError={()=>setFailed(true)} src={VIDEO}/>}
  <div className="hero-wash"/>
  <div className="hero-header" aria-hidden="true" />
  <div className="hero-content">
    <motion.h1 {...fade(0)}>AI 广告增长优化助手</motion.h1>
    <motion.p {...fade(1)}>让每一笔广告预算，<br/>投向真正会被影响的人</motion.p>
    <motion.button {...fade(2)} className="hero-cta" whileHover={reduced?{}:{scale:1.04,filter:'brightness(1.06)'}} whileTap={reduced?{}:{scale:.96}} onClick={()=>document.getElementById('analysis-workspace')?.scrollIntoView({behavior:reduced?'instant':'smooth'})}>进入分析工作台<ArrowRightCircle size={20}/></motion.button>
  </div>
 </section>
}
