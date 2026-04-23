# Issue #24: Fix  go lint warnings

**Summary**: Fix  go lint warnings

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/24

**Last updated**: 2022-02-18T23:54:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-02-18T15:47:53Z
- **Updated**: 2022-02-18T23:54:23Z
- **Closed**: 2022-02-18T23:54:23Z
- **Labels**: _none_
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 1

## Description

After running golang-ci and gofmt, the following is showed 

```bash
pkg/capacity/capacity_test.go:37:19: Error return value is not checked (errcheck)                                      
        kueue.AddToScheme(scheme)                                                                                                                                                                                                             
                         ^                  
pkg/capacity/capacity_test.go:66:23: Error return value of `cache.AddCapacity` is not checked (errcheck)               
                                        cache.AddCapacity(context.Background(), &c)                                                                                                                                                           
                                                         ^                                                                                                                                                                                    
pkg/capacity/capacity_test.go:89:26: Error return value of `cache.UpdateCapacity` is not checked (errcheck)            
                                        cache.UpdateCapacity(&c)                                                       
                                                            ^                                                                                                                                                                                 
pkg/capacity/capacity_test.go:203:19: Error return value is not checked (errcheck)
        kueue.AddToScheme(scheme)                                                                                                                                                                                                             
                         ^                                                                                                                                                                                                                    
pkg/capacity/snapshot_test.go:38:19: Error return value is not checked (errcheck)                                                                                                                                                             
        kueue.AddToScheme(scheme)                                                                                                                                                                                                             
                         ^                                                                                                                                                                                                                    
pkg/capacity/snapshot_test.go:122:20: Error return value of `cache.AddCapacity` is not checked (errcheck)              
                cache.AddCapacity(context.Background(), &cap)                                                          
                                 ^                                                                                     
pkg/queue/manager.go:61:21: Error return value of `qImpl.setProperties` is not checked (errcheck)
        qImpl.setProperties(q)                   
                           ^                                                                                           
pkg/queue/manager_test.go:394:19: Error return value of `manager.AddQueue` is not checked (errcheck)                   
                manager.AddQueue(ctx, &q)                                                                              
                                ^                          
pkg/queue/manager_test.go:452:20: Error return value of `manager.AddQueue` is not checked (errcheck)                   
                        manager.AddQueue(ctx, &q)                                                                      
                                        ^                                                                                                                                                                                                     
pkg/queue/manager_test.go:462:19: Error return value of `manager.AddQueue` is not checked (errcheck)
                manager.AddQueue(ctx, &q)                                                                              
                                ^                   
pkg/scheduler/scheduler.go:200:32: Error return value of `s.capacityCache.AssumeWorkload` is not checked (errcheck)
        s.capacityCache.AssumeWorkload(newWorkload)                                                                                                                                                                                           
                                      ^                                                                                
pkg/capacity/capacity.go:120:2: S1023: redundant `return` statement (gosimple)                                         
        return                                                                                                         
        ^                                                                                                                                                                                                                                     
pkg/capacity/snapshot_test.go:292:4: SA9003: empty branch (staticcheck)
                        if m == nil {                                                                                                                                                                                                         
                        ^
make: *** [Makefile:73: ci-lint] Error 1
```

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-18T15:48:03Z

/assign
