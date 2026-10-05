/* Per-record, atomic, revision-checked browser persistence; never stores authority. */
(function(root){
  'use strict';
  const tables=['watches','receipts','journal','folders','views','meta'];
  const request=r=>new Promise((resolve,reject)=>{r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});
  async function open(onBlocked){
    const r=indexedDB.open('midnight-express-synthetic',1);
    r.onupgradeneeded=()=>{for(const t of tables) r.result.createObjectStore(t);r.result.createObjectStore('control');};
    r.onblocked=()=>onBlocked('Storage upgrade blocked by another tab. Close its subscription page and retry.');
    const db=await request(r);
    db.onversionchange=()=>{db.close();onBlocked('Storage changed in another tab. Reload before editing.');};
    async function read(){
      const tx=db.transaction([...tables,'control'],'readonly');
      const result={}, revisionRequest=request(tx.objectStore('control').get('revision'));
      await Promise.all(tables.map(async t=>{
        const store=tx.objectStore(t), [keys,values]=await Promise.all([request(store.getAllKeys()),request(store.getAll())]);
        result[t]=Object.fromEntries(keys.map((k,i)=>[k,values[i]]));
      }));
      const revision=await revisionRequest || 0;
      return {state:revision?result:null,revision};
    }
    async function commit(before,after,revision,guard=()=>{}){
      const perform=()=>new Promise((resolve,reject)=>{
        const tx=db.transaction([...tables,'control'],'readwrite');
        let conflict=false, writeError=null;
        tx.oncomplete=()=>resolve(revision+1);
        tx.onabort=()=>reject(conflict?Error('Another tab changed the saved demo. Reload saved state before trying again.'):writeError || tx.error || Error('Storage write failed. No progress was saved.'));
        tx.onerror=()=>{};
        const check=tx.objectStore('control').get('revision');
        check.onsuccess=()=>{
          if((check.result || 0)!==revision){conflict=true;tx.abort();return;}
          try {
          guard();
          for(const t of tables){
            const store=tx.objectStore(t),old=before[t] || {},fresh=after[t] || {};
            for(const key of Object.keys(old)) if(!(key in fresh)) store.delete(key);
            for(const [key,value] of Object.entries(fresh)) if(JSON.stringify(old[key])!==JSON.stringify(value)) store.put(value,key);
          }
          tx.objectStore('control').put(revision+1,'revision');
          } catch(error) { writeError=error;tx.abort(); }
        };
      });
      return navigator.locks ? navigator.locks.request('midnight-express-demo-writer',perform) : perform();
    }
    return {read,commit,close:()=>db.close()};
  }
  root.ExpressStore={open};
})(globalThis);
