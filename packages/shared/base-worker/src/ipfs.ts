import IPFS from 'ipfs-http-client';
import fs from 'fs';

export default async (options: {url: string}) => {
    let node = await IPFS.create({url: options.url})

    console.log(await node.id())

    const getFile = async (cid: string, tmpPath: string) => {
        let content = Buffer.from('')
        let chunkCount =0;

        for await (const chunk of node.cat(cid)) {
            // if(chunkCount == 0){
            // console.log(chunk.toString())
            //     chunkCount++;
            // }
            content = Buffer.concat([content, chunk])
        }

        fs.writeFileSync(tmpPath, content)
        console.log("Gotten file", cid)
    }

    const addFile = async (file: File) => {
        console.log("Adding file")
        const result = await node.add(file)
        return result.cid;
    }
    return {
        addFile,
        getFile
    }
}
