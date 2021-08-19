import IPFS from './ipfs'
import path from 'path';
import { nanoid } from 'nanoid';

export const HiveWorker = async (
    worker_fn: (opts: {
        file: string,
        jobId: string,
        pipelineDirectory: string
    }) => Promise<boolean> 
) => {
    let {
        IPFS_URL,
        FILE_CID,
        JOB_ID,
        PIPELINE_FILES
    } = process.env;

    if(!JOB_ID) throw new Error("No JOB ID");
    if(!IPFS_URL) throw new Error("No IPFS URL specified")
    if(!FILE_CID) throw new Error("No IPFS CID specified")
    if(!PIPELINE_FILES) PIPELINE_FILES = '/mount/efs'

    const ipfsNode = await IPFS({url: IPFS_URL});

    const filePath = path.join(PIPELINE_FILES, `./${nanoid()}`)

    const cid = await ipfsNode.getFile(FILE_CID, "./test")

    const result = await worker_fn({
        file: filePath,
        jobId: JOB_ID,
        pipelineDirectory: PIPELINE_FILES
    })

    return result
   // ipfsNode.
}
