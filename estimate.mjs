export function rentalTerms(item, requestedPeriod) {
 const period=requestedPeriod??item?.period;
 const validPeriod=Boolean(item)&&(item.rates?Object.hasOwn(item.rates,period):period===item.period);
 return {period,validPeriod,price:validPeriod?(item.rates?item.rates[period]:item.price):null,maxDuration:period==='hour'?744:120};
}
export function calculateEstimate(catalog, rows) {
 const details=rows.map(row=>{
  const item=catalog.find(item=>item.id===row.id);
  const terms=rentalTerms(item,row.period);
  const valid=terms.validPeriod&&Number.isInteger(row.units)&&row.units>=1&&row.units<=100&&Number.isInteger(row.duration)&&row.duration>=1&&row.duration<=terms.maxDuration;
  return {...row,item,period:terms.period,rate:terms.price,valid,total:valid&&terms.price!=null?terms.price*row.units*row.duration:null};
 });
 return {details,valid:details.length>0&&details.every(row=>row.valid),knownTotal:details.reduce((sum,row)=>sum+(row.total??0),0),onRequest:details.filter(row=>row.valid&&row.rate==null).length,units:details.reduce((sum,row)=>sum+(row.valid?row.units:0),0)};
}
