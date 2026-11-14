export function calculateEstimate(catalog, rows) {
 const details=rows.map(row=>{
  const item=catalog.find(item=>item.id===row.id);
  const valid=Boolean(item)&&Number.isInteger(row.units)&&row.units>=1&&row.units<=100&&Number.isInteger(row.duration)&&row.duration>=1&&row.duration<=120;
  return {...row,item,valid,total:valid&&item.price!=null?item.price*row.units*row.duration:null};
 });
 return {details,valid:details.length>0&&details.every(row=>row.valid),knownTotal:details.reduce((sum,row)=>sum+(row.total??0),0),onRequest:details.filter(row=>row.valid&&row.item.price==null).length,units:details.reduce((sum,row)=>sum+(row.valid?row.units:0),0)};
}
