import test from 'node:test';
import assert from 'node:assert/strict';
import {calculateEstimate} from '../dist/estimate.mjs';
const catalog=[{id:'crane',price:3800000,period:'month'},{id:'loader',price:2500000,period:'month'},{id:'compressor',price:70000,period:'day'},{id:'spider',price:null,period:'month'}];
test('mixed equipment, fleet quantities and independent day/month periods',()=>{
 const result=calculateEstimate(catalog,[{id:'crane',units:1,duration:1},{id:'loader',units:2,duration:2},{id:'compressor',units:1,duration:3}]);
 assert.equal(result.knownTotal,14010000);assert.equal(result.units,4);assert.equal(result.onRequest,0);assert.equal(result.valid,true);
});
test('unknown prices remain explicit and do not suppress the known subtotal',()=>{
 const result=calculateEstimate(catalog,[{id:'spider',units:2,duration:1},{id:'compressor',units:1,duration:3}]);
 assert.equal(result.knownTotal,210000);assert.equal(result.onRequest,1);assert.equal(result.details[0].total,null);assert.equal(result.valid,true);
});
test('empty, missing, fractional and out-of-range values cannot be submitted',()=>{
 assert.equal(calculateEstimate(catalog,[]).valid,false);
 for(const row of [{id:'missing',units:1,duration:1},{id:'loader',units:0,duration:1},{id:'loader',units:1.5,duration:1},{id:'loader',units:101,duration:1},{id:'loader',units:1,duration:121},{id:'loader',units:1,duration:NaN}]){
  const result=calculateEstimate(catalog,[row]);assert.equal(result.valid,false);assert.equal(result.knownTotal,0);
 }
});
