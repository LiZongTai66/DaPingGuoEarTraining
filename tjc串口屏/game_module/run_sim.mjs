import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const initIvl=(await import('./_sim/ivl.js')).default;
const initVvp=(await import('./_sim/vvp.js')).default;
// This WASM port statically links system.vpi. The module directive is still
// required for emitted VVP system tasks; its dlopen notice is a port quirk.
const conf=`basedir:/\nmodule:system.vpi\ngeneration:2012\ngeneration:no-specify\nout:/out.vvp\niwidth:32\nwidthcap:65536\nfunctor:cprop\nfunctor:nodangle\nflag:DLL=vvp.tgt\n`;
async function compile(source){
  const messages=[];
  const m=await initIvl({wasmBinary:fs.readFileSync(path.join(root,'_sim/ivl.wasm')),
    print:s=>messages.push(s),printErr:s=>messages.push(s)});
  m.FS.writeFile('/ivl.conf',conf);
  m.FS.writeFile('/src.v',source);
  const code=m.callMain(['-C/ivl.conf','--','/src.v']);
  if(code!==0) throw new Error(`compile=${code}\n${messages.join('\n')}`);
  return {bytes:m.FS.readFile('/out.vvp'),messages};
}
// Complete source compilation plus isolated, accelerated game RTL tests.
const full=await compile(fs.readFileSync(path.join(root,'piano_game_complete.v'),'utf8'));
const unit=await compile(fs.readFileSync(path.join(root,'rhythm_game_core.v'),'utf8')+'\n'+fs.readFileSync(path.join(root,'tb_game.sv'),'utf8'));
const output=[];
const runtime=await initVvp({wasmBinary:fs.readFileSync(path.join(root,'_sim/vvp.wasm')),
  print:s=>output.push(s),printErr:s=>output.push(s)});
runtime.FS.writeFile('/sim.vvp',unit.bytes);
const code=runtime.callMain(['/sim.vvp']);
const report=['Complete source Icarus compilation: PASS',...full.messages,...unit.messages,...output].join('\n');
fs.writeFileSync(path.join(root,'rtl_simulation.txt'),report+'\n');
console.log(report);
if(code!==0 || !report.includes('PASS:')) process.exit(1);
const integration=await compile(fs.readFileSync(path.join(root,'piano_game_complete.v'),'utf8')+'\n'+fs.readFileSync(path.join(root,'tb_integration.sv'),'utf8'));
const second=[];
const runner=await initVvp({wasmBinary:fs.readFileSync(path.join(root,'_sim/vvp.wasm')),
  print:s=>second.push(s),printErr:s=>second.push(s)});
runner.FS.writeFile('/sim.vvp',integration.bytes);
const secondCode=runner.callMain(['/sim.vvp']);
fs.appendFileSync(path.join(root,'rtl_simulation.txt'),second.join('\n')+'\n');
console.log(second.join('\n'));
if(secondCode!==0 || !second.some(s=>s.includes('PASS integration:'))) process.exit(1);
