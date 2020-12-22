import IPFS from 'ipfs';
import fs from 'fs';
import { v4 as uuidv4 } from 'uuid';

export default async () => {
  let node = await IPFS.create()

console.log(await node.id())

 const getFile = async (cid, tmpPath) => {
    let content = Buffer.from('')
    for await (const chunk of node.cat(cid)){
      content = Buffer.concat([content, chunk])
    }

  fs.writeFileSync(tmpPath, content)
  console.log("Gotten file", cid)
}

 const addFile = async (file) => {
  console.log("Adding file")
  const id = uuidv4()
  const result = await node.add(file)
  return result.cid;
 }
  return {
    addFile,
    getFile
  } 
}
