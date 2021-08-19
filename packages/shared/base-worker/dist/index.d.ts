export declare const HiveWorker: (worker_fn: (opts: {
    file: string;
    jobId: string;
    pipelineDirectory: string;
}) => Promise<boolean>) => Promise<boolean>;
