import {promises as fs} from 'fs';
import path from 'path'
import { exec } from 'child_process';
import { HiveWorker } from 'base-worker'

HiveWorker(async (opts) => {

  return new Promise((resolve, reject) => {
    exec(`${path.resolve('')}/step_to_gltf -o ${path.join(opts.pipelineDirectory, opts.jobId)} ${opts.file}`, async (err, stdout, stderr) => {
      if(err) {
        console.error(err)
        return reject(err);
      }

      console.log(err, stdout, stderr)

      // let data = await fs.readFile(`/tmp/${json.job_id}`)
      // let result = await IPFS.addFile(data)
      resolve(true)

    })
  })

})



  // try{
  //   let json = JSON.parse(msg.content.toString())
  //   console.info("=> Processing: ", json.input_cid)
  //   await IPFS.getFile(json.input_cid, '/tmp/' + json.input_cid)


    //Run processor
    //
    // exec(``, async (err, stdout, stderr) => {
    //   if(err) {
    //     channel.nack(msg)
    //     return console.error(err)
    //   }

    //   console.log(err, stdout, stderr)

    //   let data = await fs.readFile(`/tmp/${json.job_id}`)
    //   let result = await IPFS.addFile(data)

    //   // channel.sendToQueue(outQueue, Buffer.from(JSON.stringify({
    //   //   job_id: json.job_id,
    //   //   input_cid: result.toString()
    //   // })))
    //   // channel.ack(msg)
    // })

//   }catch(e){
//     console.error(e)
//   }
// })

// main()
