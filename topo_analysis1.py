# import pandas as pd
# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
# from datetime import datetime
# import re

# # -------------------------- 1. 全局字体配置：解决字体缺失问题 --------------------------
# plt.rcParams.update({
#     "font.family": "sans-serif",  # 系统默认无衬线英文字体
#     "axes.unicode_minus": False,  # 修复负号显示
#     "font.size": 10,
#     "figure.dpi": 100
# })

# # -------------------------- 2. 全量异常数据（替换为你的完整原始文本） --------------------------
# raw_anomaly_text = """
# Time Span: 2021-03-06 00:30:00 CST → 2021-03-06 00:41:00 CST (Δ = 660 sec)
#    Total Anomalies: 197
#    🔑 Keywords: Error/Failure

#    📝 Metric App Anomalies:
#      • Entity: ServiceTest11 | Attribute: mrt
#        Timestamps: 1614962040 (2021-03-06 00:34:00 CST)
#      • Entity: ServiceTest7 | Attribute: mrt
#        Timestamps: 1614962280 (2021-03-06 00:38:00 CST)

#    📝 Metric Container Anomalies:
#      • Entity: IG01 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
#        Timestamps: 1614961860 (2021-03-06 00:31:00 CST), 1614961980 (2021-03-06 00:33:00 CST), 1614962220 (2021-03-06 00:37:00 CST), 1614962340 (2021-03-06 00:39:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: IG01 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem
#        Timestamps: 1614961920 (2021-03-06 00:32:00 CST), 1614962100 (2021-03-06 00:35:00 CST), 1614962160 (2021-03-06 00:36:00 CST)
#      • Entity: IG02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
#        Timestamps: 1614961800 (2021-03-06 00:30:00 CST), 1614962040 (2021-03-06 00:34:00 CST), 1614962280 (2021-03-06 00:38:00 CST), 1614962400 (2021-03-06 00:40:00 CST)
#      • Entity: IG02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem
#        Timestamps: 1614961860 (2021-03-06 00:31:00 CST), 1614961920 (2021-03-06 00:32:00 CST)
#      • Entity: MG01 | Attribute: JVM-Memory_7779_JVM_Memory_HeapMemoryUsage
#        Timestamps: 1614962340 (2021-03-06 00:39:00 CST)
#      • Entity: MG02 | Attribute: JVM-Memory_7779_JVM_Memory_HeapMemoryUsed
#        Timestamps: 1614961920 (2021-03-06 00:32:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_0f6f3aa7920c--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_0f6f3aa7920c--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_NetworkTxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_1bc4fc80d241--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_NetworkTxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_23bdcf67c7e3--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_MemPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_2c2336e2994f--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_2c2336e2994f--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_NetworkRxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_2d16f5b2e830--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_2d16f5b2e830--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_NetworkTxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_2fa7eaebac26--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemLimit
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_2fa7eaebac26--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_NetworkTxBytes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_350771a68ac2--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_350771a68ac2--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemLimit
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_350771a68ac2--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemUsage
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_3bf443a64876--bcou-role-st-uat-statefulset-1--bcou--UATWKR03_NetworkTxBytes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_69b53a78b2eb--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_MemLimit
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_69b53a78b2eb--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_6d83a96887c3--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_76d31070b844--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_CpuPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_76d31070b844--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_76d31070b844--bcou-role-st-uat-statefulset-1--bcou--UATWKR06_MemUsage
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_89f0c1e5346c--bcou-trace-st-uat-statefulset-0--bcou--UATWKR04_NetworkRxBytes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_94eca4f96efe--bcou-role-st-uat-statefulset-1--bcou--UATWKR04_CpuPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_94eca4f96efe--bcou-role-st-uat-statefulset-1--bcou--UATWKR04_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_94eca4f96efe--bcou-role-st-uat-statefulset-1--bcou--UATWKR04_MemUsage
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_ac3ba8476104--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_ac3ba8476104--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b2fc383d2438--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b2fc383d2438--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemLimit
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b2fc383d2438--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemUsage
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b30097144a13--bcou-trace-st-uat-statefulset-0--bcou--UATWKR04_CpuPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b30097144a13--bcou-trace-st-uat-statefulset-0--bcou--UATWKR04_NetworkTxBytes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b6760337dc49--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_b6760337dc49--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_MemLimit
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_bbc780df1fce--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_bbc780df1fce--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_NetworkTxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_NetworkTxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_cb2bbb5e3f90--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemUsage
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_cb2bbb5e3f90--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_NetworkTxBytes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_d27123361435--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_MemLimit
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_d27123361435--bcou-trace-st-uat-statefulset-1--bcou--UATWKR18_NetworkTxBytes
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_ef6cb138bb10--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_ef6cb138bb10--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_MemLimit
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_ef6cb138bb10--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_MemPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_ef6cb138bb10--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_NetworkRxBytes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_f861998c398e--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Container-DOCKER_CONTAINER_f861998c398e--bcou-role-st-uat-statefulset-0--bcou--UATWKR18_MemLimit
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: JVM-Memory_7779_JVM_Memory_HeapMemoryUsage
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: JVM-Memory_7779_JVM_Memory_NoHeapMemoryUsed
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: JVM-Operating System_7778_JVM_JVM_CPULoad
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: JVM-Runtime_7778_JVM_JVM_Uptime
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: JVM-Threads_7778_JVM_ThreadCount_Threads
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Binlog stmt cache use
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Com Delete
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Com Replace Select
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_GetConnectedStateOfMysqld
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_GetResponseTimeOfMysqld
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Handler Delete
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Handler Read First
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb buffer pool pages free
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb buffer pool pages total
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb buffer pool read ahead rnd
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb data reads
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb pages read
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb row lock time max
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Key Read Requests
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Max Used Connections
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_MaxConnections
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Open Files
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Open Tables
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Qcache Free Blocks
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Qcache Hits
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Qcache Total Blocks
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Select Full Join
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Select Full Range Join
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Sort Merge Passes
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Sort Rows
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Sort Scan
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Tc log max pages used
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Tc log page waits
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Threads Cached
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Threads Created
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_ThreadsConnected
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_----tomcat_FSInodeUsedPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-_FSInodeUsedPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-_FSUsedSpace
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-apache_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-apache_FSCapacity
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-apache_FSUsedSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-boot_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-boot_FSInodeUsedPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-boot_FSUsedSpace
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-cmbc_admin_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-cmbc_admin_FSCapacity
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-cmbc_admin_FSInodeUsedPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-cmbc_admin_FSUsedSpace
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-home_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-home_FSCapacity
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-home_FSInodeUsedPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-home_FSUsedSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSCapacity
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSInodeUsedPercent
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSUsedSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysqlbak_FSCapacity
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysqlbak_FSUsedSpace
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysqldata_FSAvailableSpace
#        Timestamps: 1614961860 (2021-03-06 00:31:00 CST), 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysqldata_FSInodeUsedPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tmp_FSAvailableSpace
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tmp_FSCapacity
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tmp_FSInodeUsedPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-usr-openv_FSCapacity
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-usr-openv_FSInodeUsedPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_CacheMem
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMTotalMem
#        Timestamps: 1614962280 (2021-03-06 00:38:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_UserMem
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_NETWORK_ens160_NETPacketsIn
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_PROCESS_apache_10001_PROCPPCount
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: OSLinux-OSLinux_SWAP_SWAP_SWPTotSwapSize
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Tomcat-Requests_7441-"http-nio-8003"_ProcessingTimeRequestInfo
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: Tomcat-Sessions_7441--UOCP_SESSIONRejectedSessions
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Tomcat-Sessions_7441--log.Home_IS_UNDEFINED_SESSIONKeepaliveCounter
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: Tomcat-Sessions_7441--log.Home_IS_UNDEFINED_SESSIONRejectedSessions
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (blocked_clients)
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (instantaneous_ops_per_sec)
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (latest_fork_usec)
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (maxmemory)
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (redis_git_dirty)
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (rejected_connections)
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (uptime_in_seconds)
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_Redis  (used_cpu_user)
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Mysql02 | Attribute: redis-Redis_6379_redis server
#        Timestamps: 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: Redis02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMUsedMemPerc
#        Timestamps: 1614961920 (2021-03-06 00:32:00 CST)
#      • Entity: Tomcat02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-_FSAvailableSpace
#        Timestamps: 1614961860 (2021-03-06 00:31:00 CST), 1614962100 (2021-03-06 00:35:00 CST), 1614962340 (2021-03-06 00:39:00 CST)
#      • Entity: apache01 | Attribute: OSLinux-CPU_CPU-0_SingleCpuidle
#        Timestamps: 1614961860 (2021-03-06 00:31:00 CST), 1614962100 (2021-03-06 00:35:00 CST), 1614962220 (2021-03-06 00:37:00 CST)
#      • Entity: apache02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-apache_FSAvailableSpace
#        Timestamps: 1614961860 (2021-03-06 00:31:00 CST), 1614962100 (2021-03-06 00:35:00 CST), 1614962220 (2021-03-06 00:37:00 CST), 1614962460 (2021-03-06 00:41:00 CST)
#      • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_CpuPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemLimit
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemPercent
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)
#      • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemUsage
#        Timestamps: 1614962100 (2021-03-06 00:35:00 CST)

#    📝 Log Anomalies:
#      • Entity: IG01 | Attribute: PatternID_117
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
#      • Entity: IG01 | Attribute: PatternID_123
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
#      • Entity: IG01 | Attribute: PatternID_29
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
#      • Entity: IG01 | Attribute: PatternID_41
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
#      • Entity: IG01 | Attribute: PatternID_47
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
#      • Entity: IG01 | Attribute: PatternID_70
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
#      • Entity: IG01 | Attribute: PatternID_96
#        Timestamps: 1614961980 (2021-03-06 00:33:00 CST)
# """

# # -------------------------- 3. 自动解析异常数据 --------------------------
# def parse_anomaly_text(text):
#     """解析原始异常文本，提取实体、指标、首个异常时间戳"""
#     anomaly_list = []
#     # 匹配实体+指标+时间戳的正则
#     entity_pattern = re.compile(r'Entity: (\w+)\s*\|\s*Attribute: ([^\n]+)')
#     timestamp_pattern = re.compile(r'Timestamps: (\d+)')
    
#     # 按行分割文本，逐行解析
#     lines = text.split('\n')
#     current_entity = None
#     current_attr = None
    
#     for line in lines:
#         line = line.strip()
#         # 匹配实体和指标
#         entity_match = entity_pattern.search(line)
#         if entity_match:
#             current_entity = entity_match.group(1)
#             current_attr = entity_match.group(2).strip()
        
#         # 匹配时间戳（提取首个时间戳）
#         if current_entity and current_attr and 'Timestamps:' in line:
#             ts_match = timestamp_pattern.search(line)
#             if ts_match:
#                 first_ts = int(ts_match.group(1))
#                 anomaly_list.append({
#                     "entity": current_entity,
#                     "attr": current_attr,
#                     "timestamp": first_ts,
#                     "time_str": datetime.fromtimestamp(first_ts).strftime("%Y-%m-%d %H:%M:%S")
#                 })
#                 # 重置，避免重复解析
#                 current_entity = None
#                 current_attr = None
    
#     return pd.DataFrame(anomaly_list)

# # 解析数据
# df_anomaly = parse_anomaly_text(raw_anomaly_text)
# print("#"*50)
# print(df_anomaly)
# print("#"*50)
# # 按实体聚合：取首个异常时间戳、统计异常指标数
# df_entity = df_anomaly.groupby('entity').agg(
#     earliest_timestamp=('timestamp', 'min'),
#     anomaly_count=('attr', 'count'),  # 实体异常指标数量
#     earliest_time=('time_str', 'first')
# ).reset_index()

# # -------------------------- 4. 构建拓扑依赖图 --------------------------
# G = nx.DiGraph()
# # 定义服务拓扑关系（保持原有逻辑）
# edges = [
#     ("apache01", "IG01"), ("apache01", "IG02"),
#     ("apache02", "IG01"), ("apache02", "IG02"),
#     ("IG01", "Tomcat02"), ("IG02", "Tomcat02"),
#     ("Tomcat02", "MG01"), ("Tomcat02", "MG02"),
#     ("MG01", "dockerA2"), ("MG02", "dockerA2"),
#     ("dockerA2", "Mysql02"),
#     ("Tomcat02", "Redis02"), ("Redis02", "Tomcat02"),
#     ("MG01", "Redis02"), ("MG02", "Redis02"), ("Redis02", "MG01"), ("Redis02", "MG02"),
# ]
# G.add_edges_from(edges)

# # -------------------------- 5. 计算根因得分（时间+拓扑+异常数量） --------------------------
# # 5.1 时间得分：异常出现越早，得分越高（0-1）
# t_min = df_entity['earliest_timestamp'].min()
# t_max = df_entity['earliest_timestamp'].max()
# df_entity['time_score'] = (t_max - df_entity['earliest_timestamp']) / (t_max - t_min) if t_max > t_min else 0

# # 5.2 拓扑得分：上游实体权重更高
# def get_reachable_nodes(entity):
#     """计算实体可影响的下游异常实体数"""
#     if entity not in G.nodes:
#         return 0
#     anomaly_entities = df_entity['entity'].tolist()
#     reachable = nx.descendants(G, entity)
#     return len([n for n in reachable if n in anomaly_entities]) + 1  # 包含自身

# # 计算拓扑特征
# df_entity['in_degree'] = df_entity['entity'].apply(lambda x: G.in_degree(x) if x in G.nodes else 0)
# df_entity['out_degree'] = df_entity['entity'].apply(lambda x: G.out_degree(x) if x in G.nodes else 0)
# df_entity['reachable_count'] = df_entity['entity'].apply(get_reachable_nodes)

# # 归一化拓扑得分（0-1）
# max_in = df_entity['in_degree'].max() if df_entity['in_degree'].max() > 0 else 1
# max_out = df_entity['out_degree'].max() if df_entity['out_degree'].max() > 0 else 1
# max_reach = df_entity['reachable_count'].max() if df_entity['reachable_count'].max() > 0 else 1

# df_entity['in_degree_score'] = 1 - (df_entity['in_degree'] / max_in)  # 入度越小（越上游）得分越高
# df_entity['out_degree_score'] = df_entity['out_degree'] / max_out    # 出度越大（影响越广）得分越高
# df_entity['reachable_score'] = df_entity['reachable_count'] / max_reach
# df_entity['topology_score'] = (df_entity['in_degree_score'] + df_entity['out_degree_score'] + df_entity['reachable_score']) / 3

# # 5.3 异常数量得分：异常指标越多，得分越高（0-1）
# max_count = df_entity['anomaly_count'].max() if df_entity['anomaly_count'].max() > 0 else 1
# df_entity['count_score'] = df_entity['anomaly_count'] / max_count

# # 5.4 最终得分（权重可调整）
# WEIGHT_TIME = 0.4
# WEIGHT_TOPOLOGY = 0.4
# WEIGHT_COUNT = 0.2
# df_entity['final_score'] = (
#     WEIGHT_TIME * df_entity['time_score'] +
#     WEIGHT_TOPOLOGY * df_entity['topology_score'] +
#     WEIGHT_COUNT * df_entity['count_score']
# )

# # 按最终得分排序
# df_entity_sorted = df_entity.sort_values('final_score', ascending=False).reset_index(drop=True)

# # -------------------------- 6. 输出分析结果 --------------------------
# print("="*80)
# print("Anomaly Root Cause Analysis Results (Ranked by Suspicion Score)")
# print("="*80)
# for idx, row in df_entity_sorted.iterrows():
#     print(f"Rank {idx+1} | Entity: {row['entity']}")
#     print(f"  - Earliest anomaly time: {row['earliest_time']}")
#     print(f"  - Anomaly metrics count: {row['anomaly_count']}")
#     print(f"  - Time score: {row['time_score']:.2f} | Topology score: {row['topology_score']:.2f} | Count score: {row['count_score']:.2f}")
#     print(f"  - Final suspicion score: {row['final_score']:.2f}")
#     print("-"*50)

# # 输出根因实体
# root_cause_entity = df_entity_sorted.iloc[0]['entity']
# print(f"\n✅ Root Cause Entity: {root_cause_entity} (Final Score: {df_entity_sorted.iloc[0]['final_score']:.2f})")

# # -------------------------- 7. 可视化（拓扑图+得分柱状图） --------------------------
# # 7.1 拓扑依赖图
# plt.figure(figsize=(12, 8))
# pos = nx.spring_layout(G, seed=42)

# # 节点样式：根因标红，其他按得分着色
# node_colors = []
# node_sizes = []
# for node in G.nodes:
#     if node == root_cause_entity:
#         node_colors.append("red")
#         node_sizes.append(800)
#     elif node in df_entity['entity'].tolist():
#         score = df_entity[df_entity['entity'] == node]['final_score'].values[0]
#         node_colors.append(plt.cm.Reds(score))
#         node_sizes.append(500 + score * 300)
#     else:
#         node_colors.append("lightgray")
#         node_sizes.append(300)

# # 绘制拓扑图
# nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes,
#         font_weight="bold", edge_color="gray", alpha=0.8)

# # 标注实体首个异常时间
# for node in df_entity['entity']:
#     if node in pos:
#         time_str = df_entity[df_entity['entity'] == node]['earliest_time'].values[0]
#         nx.draw_networkx_labels(G, pos, labels={node: f"{node}\n{time_str[-8:]}"}, font_size=8)

# plt.title("Anomaly Entity Topology (Red = Root Cause)", fontsize=14, fontweight="bold")
# plt.savefig("anomaly_root_cause_topology.png", dpi=300, bbox_inches="tight")
# plt.close()

# # 7.2 得分柱状图（Top10实体）
# plt.figure(figsize=(10, 6))
# top10 = df_entity_sorted.head(10)
# bars = plt.bar(top10['entity'], top10['final_score'], color="lightcoral")
# bars[0].set_color("red")  # 根因标红

# plt.xlabel("Entity Name", fontweight="bold")
# plt.ylabel("Final Suspicion Score", fontweight="bold")
# plt.title("Top 10 Anomaly Entities (Higher = More Likely Root Cause)", fontsize=12, fontweight="bold")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig("anomaly_root_cause_score.png", dpi=300, bbox_inches="tight")
# plt.close()

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import re

# -------------------------- 1. 全局字体配置 --------------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "font.size": 10,
    "figure.dpi": 100
})

# -------------------------- 2. 全量异常数据（包含边异常） --------------------------
raw_anomaly_text = """
🚨 Cluster #2
   Time Span: 2021-03-06 00:43:00 CST → 2021-03-06 01:00:00 CST (Δ = 1020 sec)
   Total Anomalies: 175
   🔑 Keywords: Error/Failure

   📝 Metric App Anomalies:
     • Entity: ServiceTest1 | Attribute: cnt
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest1 | Attribute: mrt
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest1 | Attribute: rr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST)
     • Entity: ServiceTest1 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST)
     • Entity: ServiceTest10 | Attribute: cnt
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest10 | Attribute: mrt
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest10 | Attribute: rr
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest10 | Attribute: sr
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest11 | Attribute: cnt
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest11 | Attribute: mrt
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest11 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963240 (2021-03-06 00:54:00 CST)
     • Entity: ServiceTest2 | Attribute: cnt
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest2 | Attribute: mrt
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest2 | Attribute: rr
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest3 | Attribute: cnt
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest3 | Attribute: mrt
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest3 | Attribute: rr
       Timestamps: 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest3 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest4 | Attribute: cnt
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest4 | Attribute: mrt
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST)
     • Entity: ServiceTest4 | Attribute: rr
       Timestamps: 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest4 | Attribute: sr
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest5 | Attribute: cnt
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest5 | Attribute: mrt
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest5 | Attribute: rr
       Timestamps: 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest5 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST)
     • Entity: ServiceTest6 | Attribute: mrt
       Timestamps: 1614963120 (2021-03-06 00:52:00 CST)
     • Entity: ServiceTest6 | Attribute: sr
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST)
     • Entity: ServiceTest7 | Attribute: cnt
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest7 | Attribute: rr
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest7 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963240 (2021-03-06 00:54:00 CST)
     • Entity: ServiceTest8 | Attribute: cnt
       Timestamps: 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest8 | Attribute: rr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963240 (2021-03-06 00:54:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: ServiceTest8 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963240 (2021-03-06 00:54:00 CST)
     • Entity: ServiceTest9 | Attribute: cnt
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST), 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest9 | Attribute: mrt
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: ServiceTest9 | Attribute: rr
       Timestamps: 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: ServiceTest9 | Attribute: sr
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963240 (2021-03-06 00:54:00 CST)

   📝 Metric Container Anomalies:
     • Entity: IG01 | Attribute: JVM-Memory_7778_JVM_Memory_HeapMemoryUsed
       Timestamps: 1614963000 (2021-03-06 00:50:00 CST)
     • Entity: IG01 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST), 1614962820 (2021-03-06 00:47:00 CST), 1614962940 (2021-03-06 00:49:00 CST), 1614963180 (2021-03-06 00:53:00 CST)
     • Entity: IG01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKTps
       Timestamps: 1614962760 (2021-03-06 00:46:00 CST)
     • Entity: IG01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKWTps
       Timestamps: 1614962700 (2021-03-06 00:45:00 CST)
     • Entity: IG02 | Attribute: JVM-Memory_7778_JVM_Memory_HeapMemoryUsage
       Timestamps: 1614962940 (2021-03-06 00:49:00 CST)
     • Entity: IG02 | Attribute: OSLinux-CPU_CPU-0_SingleCpuidle
       Timestamps: 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: IG02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
       Timestamps: 1614962640 (2021-03-06 00:44:00 CST), 1614962880 (2021-03-06 00:48:00 CST), 1614963000 (2021-03-06 00:50:00 CST), 1614963240 (2021-03-06 00:54:00 CST), 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: MG01 | Attribute: JVM-Memory_7779_JVM_Memory_HeapMemoryUsage
       Timestamps: 1614963120 (2021-03-06 00:52:00 CST)
     • Entity: Mysql01 | Attribute: Mysql-MySQL_3306_Innodb pages created
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: Mysql01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKReadWrite
       Timestamps: 1614963360 (2021-03-06 00:56:00 CST)
     • Entity: Mysql01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKWrite
       Timestamps: 1614963240 (2021-03-06 00:54:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Binlog stmt cache use
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_GetConnectedStateOfMysqld
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb row lock time avg
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Innodb row lock time max
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Max Used Connections
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_MaxConnections
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Qcache Free Blocks
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Qcache Total Blocks
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Mysql-MySQL_3306_Sort Rows
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-boot_FSInodeUsedPercent
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-boot_FSUsedSpace
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-cmbc_admin_FSInodeUsedPercent
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSAvailableSpace
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSInodeUsedPercent
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-mysql_FSUsedSpace
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-usr-openv_FSCapacity
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sda_DSKWTps
       Timestamps: 1614963000 (2021-03-06 00:50:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sda_DSKWrite
       Timestamps: 1614963000 (2021-03-06 00:50:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKAvgServ
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKPercentBusy
       Timestamps: 1614963540 (2021-03-06 00:59:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_CacheMem
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_UserMem
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Mysql02 | Attribute: Tomcat-Requests_7441-"http-nio-8003"_ErrorCountRequestInfo
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: Redis01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sda_DSKWTps
       Timestamps: 1614963120 (2021-03-06 00:52:00 CST)
     • Entity: Redis02 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKAvgServ
       Timestamps: 1614962700 (2021-03-06 00:45:00 CST)
     • Entity: Redis02 | Attribute: OSLinux-OSLinux_PROCESS_PROCESS_PROCPPMem
       Timestamps: 1614962700 (2021-03-06 00:45:00 CST)
     • Entity: Tomcat01 | Attribute: OSLinux-CPU_CPU-0_SingleCpuidle
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST)
     • Entity: Tomcat01 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963540 (2021-03-06 00:59:00 CST)
     • Entity: Tomcat01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sda_DSKRead
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: Tomcat01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKRTps
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: Tomcat01 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKRead
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: Tomcat02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
       Timestamps: 1614963360 (2021-03-06 00:56:00 CST), 1614963480 (2021-03-06 00:58:00 CST)
     • Entity: Tomcat02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST), 1614963480 (2021-03-06 00:58:00 CST), 1614963540 (2021-03-06 00:59:00 CST)
     • Entity: Tomcat02 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMTotalMem
       Timestamps: 1614963120 (2021-03-06 00:52:00 CST)
     • Entity: Tomcat03 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963540 (2021-03-06 00:59:00 CST)
     • Entity: Tomcat03 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKRTps
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: Tomcat03 | Attribute: OSLinux-OSLinux_LOCALDISK_LOCALDISK-sdb_DSKRead
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST)
     • Entity: Tomcat03 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMFreeMem
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963360 (2021-03-06 00:56:00 CST), 1614963480 (2021-03-06 00:58:00 CST), 1614963540 (2021-03-06 00:59:00 CST)
     • Entity: Tomcat04 | Attribute: OSLinux-CPU_CPU-2_SingleCpuidle
       Timestamps: 1614963480 (2021-03-06 00:58:00 CST)
     • Entity: Tomcat04 | Attribute: OSLinux-OSLinux_FILESYSTEM_-tomcat_FSAvailableSpace
       Timestamps: 1614963300 (2021-03-06 00:55:00 CST), 1614963480 (2021-03-06 00:58:00 CST)
     • Entity: Tomcat04 | Attribute: OSLinux-OSLinux_MEMORY_MEMORY_MEMTotalMem
       Timestamps: 1614962700 (2021-03-06 00:45:00 CST)
     • Entity: Tomcat04 | Attribute: OSLinux-OSLinux_NETWORK_NETWORK_TCP-FIN-WAIT
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST), 1614963360 (2021-03-06 00:56:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: apache01 | Attribute: OSLinux-CPU_CPU-0_SingleCpuidle
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)
     • Entity: apache01 | Attribute: OSLinux-CPU_CPU-1_SingleCpuidle
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST), 1614962700 (2021-03-06 00:45:00 CST)
     • Entity: apache01 | Attribute: OSLinux-CPU_CPU-3_SingleCpuidle
       Timestamps: 1614962940 (2021-03-06 00:49:00 CST), 1614963540 (2021-03-06 00:59:00 CST)
     • Entity: apache02 | Attribute: OSLinux-CPU_CPU-2_SingleCpuidle
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST), 1614962940 (2021-03-06 00:49:00 CST), 1614963180 (2021-03-06 00:53:00 CST)
     • Entity: apache02 | Attribute: OSLinux-CPU_CPU-3_SingleCpuidle
       Timestamps: 1614962940 (2021-03-06 00:49:00 CST), 1614963180 (2021-03-06 00:53:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: apache02 | Attribute: OSLinux-OSLinux_FILESYSTEM_-apache_FSAvailableSpace
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST), 1614962820 (2021-03-06 00:47:00 CST), 1614963060 (2021-03-06 00:51:00 CST), 1614963180 (2021-03-06 00:53:00 CST), 1614963420 (2021-03-06 00:57:00 CST)
     • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_CpuPercent
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST), 1614963600 (2021-03-06 01:00:00 CST)
     • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemLimit
       Timestamps: 1614963180 (2021-03-06 00:53:00 CST)
     • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemPercent
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST), 1614963600 (2021-03-06 01:00:00 CST)
     • Entity: dockerA2 | Attribute: Container-DOCKER_CONTAINER_c67422614c81--bcou-role-st-uat-statefulset-1--bcou--UATWKR02_MemUsage
       Timestamps: 1614962820 (2021-03-06 00:47:00 CST)

   📝 Log Anomalies:
     • Entity: IG01 | Attribute: PatternID_116
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST)
     • Entity: IG01 | Attribute: PatternID_134
       Timestamps: 1614963060 (2021-03-06 00:51:00 CST)
     • Entity: IG01 | Attribute: PatternID_139
       Timestamps: 1614962580 (2021-03-06 00:43:00 CST)
     • Entity: IG01 | Attribute: PatternID_153
       Timestamps: 1614962700 (2021-03-06 00:45:00 CST)
     • Entity: IG01 | Attribute: PatternID_164
       Timestamps: 1614963000 (2021-03-06 00:50:00 CST)
     • Entity: IG01 | Attribute: PatternID_53
       Timestamps: 1614963060 (2021-03-06 00:51:00 CST)
"""

# -------------------------- 3. 解析异常数据（新增边异常解析） --------------------------
def parse_anomaly_text(text):
    """
    解析包含节点异常、边异常的文本：
    - 节点异常：Entity: IG01 → 直接提取实体
    - 边异常：Entity: dockerA2->MG01 → 拆解为 source->target，同时保留边异常本身
    """
    # 存储节点异常、边异常
    node_anomalies = []
    edge_anomalies = []
    
    # 正则匹配：节点实体、边实体（source->target）、指标、时间戳
    node_entity_pattern = re.compile(r'Entity: (\w+)\s*\|\s*Attribute: ([^\n]+)')  # 节点实体
    edge_entity_pattern = re.compile(r'Entity: (\w+)->(\w+)\s*\|\s*Attribute: ([^\n]+)')  # 边实体
    timestamp_pattern = re.compile(r'Timestamps: (\d+)')
    
    lines = text.split('\n')
    current_type = None  # 'node'/'edge'
    current_source = None
    current_target = None
    current_node = None
    current_attr = None
    
    for line in lines:
        line = line.strip()
        # 匹配边异常（source->target）
        edge_match = edge_entity_pattern.search(line)
        if edge_match:
            current_type = 'edge'
            current_source = edge_match.group(1)
            current_target = edge_match.group(2)
            current_attr = edge_match.group(3).strip()
            continue
        
        # 匹配节点异常
        node_match = node_entity_pattern.search(line)
        if node_match:
            current_type = 'node'
            current_node = node_match.group(1)
            current_attr = node_match.group(2).strip()
            continue
        
        # 匹配时间戳并存储
        if 'Timestamps:' in line and current_attr:
            ts_match = timestamp_pattern.search(line)
            if ts_match:
                ts = int(ts_match.group(1))
                time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                # 存储边异常
                if current_type == 'edge' and current_source and current_target:
                    edge_anomalies.append({
                        "source": current_source,
                        "target": current_target,
                        "attr": current_attr,
                        "timestamp": ts,
                        "time_str": time_str
                    })
                # 存储节点异常
                elif current_type == 'node' and current_node:
                    node_anomalies.append({
                        "entity": current_node,
                        "attr": current_attr,
                        "timestamp": ts,
                        "time_str": time_str
                    })
                # 重置状态
                current_type = None
                current_source = current_target = current_node = current_attr = None
    
    # 转为DataFrame
    df_node = pd.DataFrame(node_anomalies)
    df_edge = pd.DataFrame(edge_anomalies)
    return df_node, df_edge

# 解析节点异常、边异常
df_node, df_edge = parse_anomaly_text(raw_anomaly_text)

# -------------------------- 4. 构建增强拓扑图（融入边异常） --------------------------
# 基础拓扑边
base_edges = [
    ("apache01", "IG01"), ("apache01", "IG02"),
    ("apache02", "IG01"), ("apache02", "IG02"),
    ("IG01", "Tomcat02"), ("IG02", "Tomcat02"),
    ("Tomcat02", "MG01"), ("Tomcat02", "MG02"),
    ("MG01", "dockerA2"), ("MG02", "dockerA2"),
    ("dockerA2", "Mysql02"),
    ("Tomcat02", "Redis02"), ("Redis02", "Tomcat02"),
    ("MG01", "Redis02"), ("MG02", "Redis02"), ("Redis02", "MG01"), ("Redis02", "MG02"),
]

# 初始化拓扑图
G = nx.DiGraph()
G.add_edges_from(base_edges)

# 给拓扑图的边添加异常属性（标记哪些边有异常、异常时间）
# 初始化边属性
for u, v in G.edges:
    G.edges[u, v]['has_anomaly'] = False
    G.edges[u, v]['anomaly_timestamp'] = None
    G.edges[u, v]['anomaly_attr'] = None

# 把边异常标记到拓扑图中
for _, row in df_edge.iterrows():
    s, t = row['source'], row['target']
    # 如果边不存在，添加该边到拓扑图
    if not G.has_edge(s, t):
        G.add_edge(s, t)
    # 标记边异常属性
    G.edges[s, t]['has_anomaly'] = True
    G.edges[s, t]['anomaly_timestamp'] = row['timestamp']
    G.edges[s, t]['anomaly_attr'] = row['attr']
    G.edges[s, t]['anomaly_time_str'] = row['time_str']

# -------------------------- 5. 聚合节点得分（融入边异常影响） --------------------------
# 5.1 聚合节点异常（取首个异常时间、异常数量）
if not df_node.empty:
    df_node_agg = df_node.groupby('entity').agg(
        node_earliest_ts=('timestamp', 'min'),
        node_anomaly_count=('attr', 'count'),
        node_earliest_time=('time_str', 'first')
    ).reset_index()
else:
    df_node_agg = pd.DataFrame(columns=['entity', 'node_earliest_ts', 'node_anomaly_count', 'node_earliest_time'])

# 5.2 计算节点的边异常影响得分
def get_edge_anomaly_score(entity):
    """
    计算节点的边异常影响得分：
    - 入边/出边有异常的数量
    - 边异常出现的时间（越早得分越高）
    """
    # 该节点的所有入边、出边
    in_edges = list(G.in_edges(entity))
    out_edges = list(G.out_edges(entity))
    all_edges = in_edges + out_edges
    
    edge_anomaly_count = 0
    edge_earliest_ts = None
    
    for u, v in all_edges:
        if G.edges[u, v]['has_anomaly']:
            edge_anomaly_count += 1
            ts = G.edges[u, v]['anomaly_timestamp']
            if edge_earliest_ts is None or ts < edge_earliest_ts:
                edge_earliest_ts = ts
    
    return {
        "edge_anomaly_count": edge_anomaly_count,
        "edge_earliest_ts": edge_earliest_ts,
        "edge_earliest_time": datetime.fromtimestamp(edge_earliest_ts).strftime("%Y-%m-%d %H:%M:%S") if edge_earliest_ts else None
    }

# 收集所有实体（拓扑图中的节点）
all_entities = list(G.nodes)
df_entity = pd.DataFrame({"entity": all_entities})

# 合并节点异常数据
df_entity = df_entity.merge(df_node_agg, on='entity', how='left').fillna({
    "node_anomaly_count": 0,
    "node_earliest_ts": np.inf  # 无节点异常则时间设为无穷大
})

# 计算边异常影响得分
edge_scores = df_entity['entity'].apply(get_edge_anomaly_score)
df_edge_score = pd.json_normalize(edge_scores)
df_entity = pd.concat([df_entity, df_edge_score], axis=1).fillna({
    "edge_anomaly_count": 0,
    "edge_earliest_ts": np.inf
})

# 5.3 计算实体的综合最早异常时间（节点异常/边异常取更早的）
def get_earliest_ts(row):
    ts_list = [row['node_earliest_ts'], row['edge_earliest_ts']]
    ts_list = [ts for ts in ts_list if ts != np.inf]
    return min(ts_list) if ts_list else None

df_entity['earliest_timestamp'] = df_entity.apply(get_earliest_ts, axis=1)
df_entity['has_anomaly'] = df_entity.apply(
    lambda x: x['node_anomaly_count'] > 0 or x['edge_anomaly_count'] > 0, axis=1
)

# 过滤掉无异常的实体
df_entity = df_entity[df_entity['has_anomaly']].reset_index(drop=True)
if df_entity.empty:
    print("No anomaly entities found!")
    exit()

# 补充最早异常时间字符串
df_entity['earliest_time'] = df_entity['earliest_timestamp'].apply(
    lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x else None
)

# -------------------------- 6. 计算根因综合得分 --------------------------
# 6.1 时间得分（节点/边异常越早，得分越高）
t_min = df_entity['earliest_timestamp'].min()
t_max = df_entity['earliest_timestamp'].max()
df_entity['time_score'] = (t_max - df_entity['earliest_timestamp']) / (t_max - t_min) if t_max > t_min else 0

# 6.2 拓扑得分（上游+影响范围）
def get_reachable_nodes(entity):
    anomaly_entities = df_entity['entity'].tolist()
    reachable = nx.descendants(G, entity)
    return len([n for n in reachable if n in anomaly_entities]) + 1

df_entity['in_degree'] = df_entity['entity'].apply(lambda x: G.in_degree(x))
df_entity['out_degree'] = df_entity['entity'].apply(lambda x: G.out_degree(x))
df_entity['reachable_count'] = df_entity['entity'].apply(get_reachable_nodes)

# 归一化拓扑得分
max_in = df_entity['in_degree'].max() if df_entity['in_degree'].max() > 0 else 1
max_out = df_entity['out_degree'].max() if df_entity['out_degree'].max() > 0 else 1
max_reach = df_entity['reachable_count'].max() if df_entity['reachable_count'].max() > 0 else 1

df_entity['in_degree_score'] = 1 - (df_entity['in_degree'] / max_in)
df_entity['out_degree_score'] = df_entity['out_degree'] / max_out
df_entity['reachable_score'] = df_entity['reachable_count'] / max_reach
df_entity['topology_score'] = (df_entity['in_degree_score'] + df_entity['out_degree_score'] + df_entity['reachable_score']) / 3

# 6.3 异常数量得分（节点异常+边异常总数）
df_entity['total_anomaly_count'] = df_entity['node_anomaly_count'] + df_entity['edge_anomaly_count']
max_total_count = df_entity['total_anomaly_count'].max() if df_entity['total_anomaly_count'].max() > 0 else 1
df_entity['count_score'] = df_entity['total_anomaly_count'] / max_total_count

# 6.4 最终得分（权重可调整）
WEIGHT_TIME = 0.4
WEIGHT_TOPOLOGY = 0.3
WEIGHT_COUNT = 0.3
df_entity['final_score'] = (
    WEIGHT_TIME * df_entity['time_score'] +
    WEIGHT_TOPOLOGY * df_entity['topology_score'] +
    WEIGHT_COUNT * df_entity['count_score']
)

# 按最终得分排序
df_entity_sorted = df_entity.sort_values('final_score', ascending=False).reset_index(drop=True)

# -------------------------- 7. 输出分析结果（包含边异常） --------------------------
print("="*80)
print("Anomaly Root Cause Analysis (Including Edge Anomalies)")
print("="*80)

# 先输出边异常详情
if not df_edge.empty:
    print("📌 Edge Anomalies Details:")
    for _, row in df_edge.iterrows():
        print(f"  - Edge: {row['source']}->{row['target']} | Attr: {row['attr']} | Time: {row['time_str']}")
    print("-"*50)

# 输出实体根因排名
for idx, row in df_entity_sorted.iterrows():
    print(f"Rank {idx+1} | Entity: {row['entity']}")
    print(f"  - Earliest anomaly time: {row['earliest_time']}")
    print(f"  - Node anomalies: {row['node_anomaly_count']} | Edge anomalies: {row['edge_anomaly_count']}")
    print(f"  - Time score: {row['time_score']:.2f} | Topology score: {row['topology_score']:.2f} | Count score: {row['count_score']:.2f}")
    print(f"  - Final suspicion score: {row['final_score']:.2f}")
    print("-"*50)

# 输出根因实体
root_cause_entity = df_entity_sorted.iloc[0]['entity']
print(f"\n✅ Root Cause Entity: {root_cause_entity} (Final Score: {df_entity_sorted.iloc[0]['final_score']:.2f})")

# -------------------------- 8. 可视化（标记边异常） --------------------------
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)

# 绘制节点：根因标红，其他按得分着色
node_colors = []
node_sizes = []
for node in G.nodes:
    if node == root_cause_entity:
        node_colors.append("red")
        node_sizes.append(800)
    elif node in df_entity['entity'].tolist():
        score = df_entity[df_entity['entity'] == node]['final_score'].values[0]
        node_colors.append(plt.cm.Reds(score))
        node_sizes.append(500 + score * 300)
    else:
        node_colors.append("lightgray")
        node_sizes.append(300)

# 绘制边：异常边标红加粗，正常边灰色
edge_colors = []
edge_widths = []
for u, v in G.edges:
    if G.edges[u, v]['has_anomaly']:
        edge_colors.append("red")
        edge_widths.append(3)
    else:
        edge_colors.append("gray")
        edge_widths.append(1)

# 绘制拓扑图
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes,
        edge_color=edge_colors, width=edge_widths, font_weight="bold", alpha=0.8)

# 标注节点最早异常时间
for node in df_entity['entity']:
    if node in pos:
        time_str = df_entity[df_entity['entity'] == node]['earliest_time'].values[0]
        nx.draw_networkx_labels(G, pos, labels={node: f"{node}\n{time_str[-8:]}"}, font_size=8)

# 标注边异常（可选）
for u, v in G.edges:
    if G.edges[u, v]['has_anomaly']:
        mid_pos = ((pos[u][0] + pos[v][0])/2, (pos[u][1] + pos[v][1])/2)
        plt.text(mid_pos[0], mid_pos[1]+0.05, "⚠️", fontsize=12, ha='center')

plt.title("Anomaly Topology (Red Node=Root Cause, Red Edge=Edge Anomaly)", fontsize=14, fontweight="bold")
plt.savefig("anomaly_root_cause_with_edge.png", dpi=300, bbox_inches="tight")
plt.close()