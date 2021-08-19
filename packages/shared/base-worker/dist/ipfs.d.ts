import IPFS from 'ipfs-http-client';
declare const _default: (options: {
    url: string;
}) => Promise<{
    addFile: (file: File) => Promise<IPFS.CID>;
    getFile: (cid: string, tmpPath: string) => Promise<void>;
}>;
export default _default;
