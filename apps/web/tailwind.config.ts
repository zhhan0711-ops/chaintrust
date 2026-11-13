import type { Config } from 'tailwindcss';
const config: Config = { content:['./app/**/*.{ts,tsx}','./components/**/*.{ts,tsx}'], theme:{extend:{colors:{ink:'#070A18',panel:'#10152D',violet:'#8B5CF6',electric:'#38BDF8'}}}, plugins:[] };
export default config;
