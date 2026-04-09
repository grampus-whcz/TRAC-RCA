import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import re

# -------------------------- 1. Global Configuration --------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.unicode_minus": False,
    "font.size": 10,
    "figure.dpi": 100
})

# Core RCA Configuration
CONCENTRATION_WINDOW_MINUTES = 3  # Anomaly concentration time window (minutes after fault start)
ANOMALY_THRESHOLD = 2             # Minimum anomalies for root cause candidate
FALLBACK_THRESHOLD = 1            # Fallback threshold if no candidates meet main threshold
# Score Weights
WEIGHT_TIME = 0.4
WEIGHT_TOPOLOGY = 0.3
WEIGHT_COUNT = 0.3

# -------------------------- 2. Anomaly Data Input --------------------------
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

# -------------------------- 3. Anomaly Parsing Function --------------------------
def parse_anomaly_text(text):
    """
    Parse anomaly text data into node and edge anomaly DataFrames
    Ensures complete column structure even with empty data
    """
    node_anomalies = []  # Store node anomalies
    edge_anomalies = []  # Store edge anomalies

    # Regular expression patterns
    node_pattern = re.compile(r'Entity: (\w+)\s*\|\s*Attribute: ([^\n]+)')
    edge_pattern = re.compile(r'Entity: (\w+)->(\w+)\s*\|\s*Attribute: ([^\n]+)')
    ts_pattern = re.compile(r'Timestamps: (\d+)')

    lines = text.split('\n')
    # State variables to track current anomaly parsing
    current_type = None  # 'node'/'edge'/None
    current_node = None
    current_source = current_target = None
    current_attr = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match edge anomalies (higher priority than node)
        edge_match = edge_pattern.search(line)
        if edge_match:
            current_type = 'edge'
            current_source = edge_match.group(1)
            current_target = edge_match.group(2)
            current_attr = edge_match.group(3).strip()
            continue

        # Match node anomalies
        node_match = node_pattern.search(line)
        if node_match:
            current_type = 'node'
            current_node = node_match.group(1)
            current_attr = node_match.group(2).strip()
            continue

        # Match timestamp and complete anomaly record
        if 'Timestamps:' in line and current_attr and current_type:
            ts_match = ts_pattern.search(line)
            if ts_match:
                ts = int(ts_match.group(1))
                time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                # Add edge anomaly
                if current_type == 'edge' and current_source and current_target:
                    edge_anomalies.append({
                        "source": current_source,
                        "target": current_target,
                        "attr": current_attr,
                        "timestamp": ts,
                        "time_str": time_str
                    })
                # Add node anomaly
                elif current_type == 'node' and current_node:
                    node_anomalies.append({
                        "entity": current_node,
                        "attr": current_attr,
                        "timestamp": ts,
                        "time_str": time_str
                    })
                # Reset state to prevent cross-line contamination
                current_type = current_node = current_source = current_target = current_attr = None

    # Force column structure to prevent KeyError even with empty data
    df_node = pd.DataFrame(node_anomalies, columns=['entity', 'attr', 'timestamp', 'time_str'])
    df_edge = pd.DataFrame(edge_anomalies, columns=['source', 'target', 'attr', 'timestamp', 'time_str'])
    return df_node, df_edge

# -------------------------- 4. Concentrated Anomaly Filtering --------------------------
def filter_concentrated_anomalies(df_node, df_edge):
    """
    Filter entities with concentrated anomalies to generate root cause candidates
    Compatible with node-only/edge-only/mixed anomaly scenarios
    """
    # Step 1: Extract all valid timestamps to determine fault start time (T0)
    all_ts = []
    # Node anomaly timestamps
    if not df_node.empty and 'timestamp' in df_node.columns:
        all_ts.extend(df_node['timestamp'].dropna().astype(int).tolist())
    # Edge anomaly timestamps
    if not df_edge.empty and 'timestamp' in df_edge.columns:
        all_ts.extend(df_edge['timestamp'].dropna().astype(int).tolist())
    
    # Terminate if no anomaly data
    if not all_ts:
        print("❌ No anomaly data parsed, analysis terminated")
        return None, None, None, None, None
    T0 = min(all_ts)
    T_window = T0 + CONCENTRATION_WINDOW_MINUTES * 60  # Window end time (seconds)

    # Step 2: Filter anomalies within time window
    df_node_window = df_node[df_node['timestamp'] <= T_window].copy() if not df_node.empty else df_node
    df_edge_window = df_edge[df_edge['timestamp'] <= T_window].copy() if not df_edge.empty else df_edge

    # Step 3: Count total anomalies per entity (node + associated edge anomalies)
    # 3.1 Count node anomalies
    node_count = pd.DataFrame(columns=['entity', 'node_anomaly_count'])
    if not df_node_window.empty and 'entity' in df_node_window.columns:
        node_count = df_node_window.groupby('entity').size().reset_index(name='node_anomaly_count')

    # 3.2 Count edge anomalies (empty for node-only scenario)
    edge_count = pd.DataFrame(columns=['entity', 'edge_anomaly_count'])
    if not df_edge_window.empty and all(col in df_edge_window.columns for col in ['source', 'target']):
        # Count edge anomalies for source entities
        source_count = df_edge_window.groupby('source').size().reset_index(name='edge_anomaly_count')
        source_count.columns = ['entity', 'edge_anomaly_count']
        # Count edge anomalies for target entities
        target_count = df_edge_window.groupby('target').size().reset_index(name='edge_anomaly_count')
        target_count.columns = ['entity', 'edge_anomaly_count']
        # Merge and sum source/target counts
        edge_count = pd.concat([source_count, target_count], ignore_index=True)
        edge_count = edge_count.groupby('entity')['edge_anomaly_count'].sum().reset_index()

    # 3.3 Merge all entities and calculate total anomalies
    all_entities = set()
    if not node_count.empty:
        all_entities.update(node_count['entity'].tolist())
    if not edge_count.empty:
        all_entities.update(edge_count['entity'].tolist())
    all_entities = list(all_entities)
    
    # Terminate if no associated entities
    if not all_entities:
        print("❌ No anomaly-associated entities parsed, analysis terminated")
        return None, None, None, None, None

    # Merge node/edge counts (fill 0 for no anomalies)
    df_entity = pd.DataFrame({'entity': all_entities})
    df_entity = df_entity.merge(node_count, on='entity', how='left').fillna({'node_anomaly_count': 0})
    df_entity = df_entity.merge(edge_count, on='entity', how='left').fillna({'edge_anomaly_count': 0})
    # Total anomalies = node anomalies + associated edge anomalies
    df_entity['total_anomaly_window'] = df_entity['node_anomaly_count'] + df_entity['edge_anomaly_count']

    # Step 4: Filter root cause candidates (fallback if empty)
    df_candidate = df_entity[df_entity['total_anomaly_window'] >= ANOMALY_THRESHOLD].copy()
    if df_candidate.empty:
        df_candidate = df_entity[df_entity['total_anomaly_window'] >= FALLBACK_THRESHOLD].copy()
        print(f"⚠️  No entities meet threshold {ANOMALY_THRESHOLD}, falling back to threshold {FALLBACK_THRESHOLD}")

    return df_node_window, df_edge_window, df_candidate, T0, T_window

# -------------------------- 5. Topology Graph Construction --------------------------
def build_topo_graph(df_edge_window):
    """
    Build microservice topology graph and mark anomalous edges
    - Edge-only/mixed scenarios: Mark anomalous edges
    - Node-only scenarios: Show base topology only
    """
    # Base microservice topology edges (fixed)
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

    G = nx.DiGraph()
    G.add_edges_from(base_edges)

    # Initialize edge attributes (default: no anomaly)
    for u, v in G.edges:
        G.edges[u, v]['has_anomaly'] = False
        G.edges[u, v]['anomaly_timestamp'] = None
        G.edges[u, v]['anomaly_time_str'] = None

    # Mark anomalous edges in window (no operation for node-only scenario)
    if not df_edge_window.empty and all(col in df_edge_window.columns for col in ['source', 'target', 'timestamp', 'time_str']):
        for _, row in df_edge_window.iterrows():
            s, t = row['source'], row['target']
            # Add edge to topology if not exists (compatible with unknown edges)
            if not G.has_edge(s, t):
                G.add_edge(s, t)
            # Mark anomaly attributes
            G.edges[s, t]['has_anomaly'] = True
            G.edges[s, t]['anomaly_timestamp'] = row['timestamp']
            G.edges[s, t]['anomaly_time_str'] = row['time_str']

    return G

# -------------------------- 6. Candidate Entity Feature Enhancement --------------------------
def enrich_candidate_feat(df_candidate, df_node_window, df_edge_window, G, T0, T_window):
    """
    Enhance candidate entities with:
    - Earliest anomaly time
    - Topological features (in-degree/out-degree/reachable downstream entities)
    """
    df_enriched = df_candidate.copy()

    # Step 1: Add earliest anomaly time (compatible with all scenarios)
    # 1.1 Earliest node anomaly time (fixed merge key issue)
    node_earliest = pd.DataFrame(columns=['entity', 'node_earliest_ts', 'node_earliest_time'])
    if not df_node_window.empty and all(col in df_node_window.columns for col in ['entity', 'timestamp', 'time_str']):
        # Get minimum timestamp per entity
        node_earliest = df_node_window.groupby('entity')['timestamp'].min().reset_index(name='node_earliest_ts')
        # Create time map to get corresponding time string
        time_map = df_node_window[['entity', 'timestamp', 'time_str']].drop_duplicates(subset=['entity', 'timestamp'])
        # Merge with correct keys (fix KeyError issue)
        node_earliest = node_earliest.merge(
            time_map,
            left_on=['entity', 'node_earliest_ts'],  # Left key (node_earliest column)
            right_on=['entity', 'timestamp'],         # Right key (df_node_window column)
            how='left'
        ).drop(columns=['timestamp']).rename(columns={'time_str': 'node_earliest_time'})

    # 1.2 Earliest edge anomaly time (empty for node-only scenario)
    edge_earliest = pd.DataFrame(columns=['entity', 'edge_earliest_ts', 'edge_earliest_time'])
    if not df_edge_window.empty and all(col in df_edge_window.columns for col in ['source', 'target', 'timestamp', 'time_str']):
        # Earliest edge anomaly for source entities
        source_earliest = df_edge_window.groupby('source')['timestamp'].min().reset_index(name='edge_earliest_ts')
        source_earliest = source_earliest.merge(
            df_edge_window[['source', 'timestamp', 'time_str']].drop_duplicates(),
            left_on=['source', 'edge_earliest_ts'],
            right_on=['source', 'timestamp'],
            how='left'
        ).drop(columns=['timestamp']).rename(columns={'source': 'entity', 'time_str': 'edge_earliest_time'})[['entity', 'edge_earliest_ts', 'edge_earliest_time']]

        # Earliest edge anomaly for target entities
        target_earliest = df_edge_window.groupby('target')['timestamp'].min().reset_index(name='edge_earliest_ts')
        target_earliest = target_earliest.merge(
            df_edge_window[['target', 'timestamp', 'time_str']].drop_duplicates(),
            left_on=['target', 'edge_earliest_ts'],
            right_on=['target', 'timestamp'],
            how='left'
        ).drop(columns=['timestamp']).rename(columns={'target': 'entity', 'time_str': 'edge_earliest_time'})[['entity', 'edge_earliest_ts', 'edge_earliest_time']]

        # Merge source/target and get minimum timestamp
        edge_earliest = pd.concat([source_earliest, target_earliest], ignore_index=True)
        edge_earliest = edge_earliest.groupby('entity').agg(
            edge_earliest_ts=('edge_earliest_ts', 'min'),
            edge_earliest_time=('edge_earliest_time', 'first')
        ).reset_index()

    # Merge node/edge earliest times (fill inf for no data)
    df_enriched = df_enriched.merge(node_earliest, on='entity', how='left').fillna({'node_earliest_ts': np.inf})
    df_enriched = df_enriched.merge(edge_earliest, on='entity', how='left').fillna({'edge_earliest_ts': np.inf})

    # Calculate comprehensive earliest time
    def get_earliest(row):
        ts_list = [row['node_earliest_ts'], row['edge_earliest_ts']]
        ts_list = [ts for ts in ts_list if ts != np.inf and not pd.isna(ts)]
        return min(ts_list) if ts_list else None
    df_enriched['earliest_timestamp'] = df_enriched.apply(get_earliest, axis=1)

    # Format timestamp to string (handle inf/NaN)
    def ts2str(ts):
        if ts is None or ts == np.inf or pd.isna(ts):
            return "N/A"
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    df_enriched['node_earliest_time'] = df_enriched['node_earliest_ts'].apply(ts2str)
    df_enriched['edge_earliest_time'] = df_enriched['edge_earliest_ts'].apply(ts2str)
    df_enriched['earliest_time'] = df_enriched['earliest_timestamp'].apply(ts2str)

    # Step 2: Add topological features
    def get_reachable(entity):
        """Calculate number of reachable downstream candidate entities"""
        if entity not in G.nodes:
            return 0
        reachable_nodes = nx.descendants(G, entity)
        candidate_entities = df_enriched['entity'].tolist()
        # Include self in count
        return len([n for n in reachable_nodes if n in candidate_entities]) + 1

    # In-degree/out-degree (0 if entity not in topology)
    df_enriched['in_degree'] = df_enriched['entity'].apply(lambda x: G.in_degree(x) if x in G.nodes else 0)
    df_enriched['out_degree'] = df_enriched['entity'].apply(lambda x: G.out_degree(x) if x in G.nodes else 0)
    # Reachable downstream candidate entities
    df_enriched['reachable_count'] = df_enriched['entity'].apply(get_reachable)

    return df_enriched

# -------------------------- 7. Root Cause Score Calculation --------------------------
def calculate_rca_score(df_enriched):
    """
    Calculate root cause score with normalization only within candidate set
    Score components: time (40%) + topology (30%) + anomaly count (30%)
    """
    df_scored = df_enriched.copy()
    # Filter entities with valid earliest timestamp
    df_scored = df_scored[df_scored['earliest_timestamp'].notna() & (df_scored['earliest_timestamp'] != np.inf)].copy()
    if df_scored.empty:
        print("❌ No valid anomaly times in candidate set, cannot calculate scores")
        return None

    # Feature 1: Time score (earlier anomalies = higher score, 0-1)
    t_min = df_scored['earliest_timestamp'].min()
    t_max = df_scored['earliest_timestamp'].max()
    df_scored['time_score'] = 1.0 if t_min == t_max else (t_max - df_scored['earliest_timestamp']) / (t_max - t_min)

    # Feature 2: Topology score (upstream + influence scope, 0-1)
    max_in = df_scored['in_degree'].max() if df_scored['in_degree'].max() > 0 else 1
    max_out = df_scored['out_degree'].max() if df_scored['out_degree'].max() > 0 else 1
    max_reach = df_scored['reachable_count'].max() if df_scored['reachable_count'].max() > 0 else 1
    
    # In-degree score: lower = more upstream = higher score
    df_scored['in_degree_score'] = 1 - (df_scored['in_degree'] / max_in)
    # Out-degree score: higher = broader influence = higher score
    df_scored['out_degree_score'] = df_scored['out_degree'] / max_out
    # Reachability score: higher = more downstream impact = higher score
    df_scored['reachable_score'] = df_scored['reachable_count'] / max_reach
    # Combined topology score (average of three components)
    df_scored['topology_score'] = (df_scored['in_degree_score'] + df_scored['out_degree_score'] + df_scored['reachable_score']) / 3

    # Feature 3: Anomaly count score (more anomalies = higher score, 0-1)
    max_count = df_scored['total_anomaly_window'].max() if df_scored['total_anomaly_window'].max() > 0 else 1
    df_scored['count_score'] = df_scored['total_anomaly_window'] / max_count

    # Final root cause score (weighted sum)
    df_scored['final_score'] = (
        WEIGHT_TIME * df_scored['time_score'] +
        WEIGHT_TOPOLOGY * df_scored['topology_score'] +
        WEIGHT_COUNT * df_scored['count_score']
    )

    # Sort by final score (descending) and round to 2 decimal places
    df_scored = df_scored.sort_values('final_score', ascending=False).reset_index(drop=True)
    score_cols = ['time_score', 'topology_score', 'count_score', 'final_score', 
                 'in_degree_score', 'out_degree_score', 'reachable_score']
    df_scored[score_cols] = df_scored[score_cols].round(2)

    return df_scored

# -------------------------- 8. Topology Visualization --------------------------
def visualize_topo(G, df_scored, T0, T_window):
    """
    Visualize topology graph with color-coding:
    - Red node: Root cause entity (highest score)
    - Red thick edges: Anomalous edges
    - Gradient red nodes: Candidate entities (darker = higher score)
    - Gray nodes: Non-anomalous entities
    """
    plt.figure(figsize=(14, 10))
    # Fixed layout seed for consistent visualization
    pos = nx.spring_layout(G, seed=42, k=0.8)

    # Draw nodes with color coding
    node_colors = []
    node_sizes = []
    root_cause = df_scored.iloc[0]['entity'] if not df_scored.empty else None
    candidate_entities = df_scored['entity'].tolist() if not df_scored.empty else []
    
    for node in G.nodes:
        if node == root_cause:
            # Root cause: solid red + large size
            node_colors.append('red')
            node_sizes.append(800)
        elif node in candidate_entities:
            # Candidates: gradient red based on score
            score = df_scored[df_scored['entity'] == node]['final_score'].values[0]
            node_colors.append(plt.cm.Reds(0.5 + score * 0.5))  # Darker = higher score
            node_sizes.append(500 + score * 300)
        else:
            # Non-anomalous: light gray + small size
            node_colors.append('lightgray')
            node_sizes.append(300)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)

    # Draw edges with anomaly marking
    edge_colors = []
    edge_widths = []
    for u, v in G.edges:
        if G.edges[u, v]['has_anomaly']:
            # Anomalous edge: solid red + thick
            edge_colors.append('red')
            edge_widths.append(3)
        else:
            # Normal edge: light gray + thin
            edge_colors.append('gray')
            edge_widths.append(1)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, 
                          alpha=0.6, arrows=True, arrowstyle='->', arrowsize=10)

    # Draw node labels (show earliest anomaly time for candidates)
    node_labels = {}
    for node in G.nodes:
        if node in candidate_entities:
            time_str = df_scored[df_scored['entity'] == node]['earliest_time'].values[0]
            # Show only time part (HH:MM:SS) for compactness
            node_labels[node] = f"{node}\n{time_str[-8:]}" if time_str != "N/A" else node
        else:
            node_labels[node] = node
    nx.draw_networkx_labels(G, pos, node_labels, font_size=9, font_weight='bold')

    # Mark anomalous edges with warning symbol
    for u, v in G.edges:
        if G.edges[u, v]['has_anomaly']:
            mid_pos = ((pos[u][0] + pos[v][0])/2, (pos[u][1] + pos[v][1])/2)
            plt.text(mid_pos[0], mid_pos[1]+0.05, '⚠️', fontsize=12, ha='center', color='red')

    # Graph title with time window
    t0_str = datetime.fromtimestamp(T0).strftime("%Y-%m-%d %H:%M:%S") if T0 else "Unknown"
    tw_str = datetime.fromtimestamp(T_window).strftime("%Y-%m-%d %H:%M:%S") if T_window else "Unknown"
    plt.title(
        f"Microservice RCA Topology Graph\nConcentration Window: {t0_str} ~ {tw_str}\nRed Node=Root Cause | Red Thick Edge=Anomalous Edge | ⚠️=Edge Anomaly",
        fontsize=14, fontweight='bold', pad=20
    )
    plt.axis('off')  # Hide axes
    plt.tight_layout()
    # Save visualization (high resolution)
    plt.savefig("rca_topo_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n📊 Topology visualization saved as: rca_topo_analysis.png")

# -------------------------- 9. Main Function (Orchestration) --------------------------
def main():
    # Step 1: Parse anomaly data
    df_node, df_edge = parse_anomaly_text(raw_anomaly_text)
    print(f"📥 Anomaly parsing result: {len(df_node)} node anomalies | {len(df_edge)} edge anomalies")

    # Step 2: Filter concentrated anomalies to get candidates
    res = filter_concentrated_anomalies(df_node, df_edge)
    if any(r is None for r in res):
        return
    df_node_window, df_edge_window, df_candidate, T0, T_window = res
    print(f"🔍 Anomaly concentration window: {datetime.fromtimestamp(T0)} ~ {datetime.fromtimestamp(T_window)} ({CONCENTRATION_WINDOW_MINUTES} minutes)")
    print(f"🎯 Root cause candidates: {len(df_candidate)} entities")

    # Step 3: Build topology graph
    G = build_topo_graph(df_edge_window)

    # Step 4: Enhance candidate features
    df_enriched = enrich_candidate_feat(df_candidate, df_node_window, df_edge_window, G, T0, T_window)

    # Step 5: Calculate RCA scores
    df_scored = calculate_rca_score(df_enriched)
    if df_scored is None:
        return

    # Step 6: Print analysis results
    print("="*100)
    print(f"📈 Root Cause Analysis Results (sorted by final score) - {CONCENTRATION_WINDOW_MINUTES}min Concentration Window")
    print("="*100)
    # Select key columns for display
    show_cols = [
        'entity', 'earliest_time', 'node_anomaly_count', 'edge_anomaly_count',
        'total_anomaly_window', 'time_score', 'topology_score', 'count_score', 'final_score'
    ]
    for idx, row in df_scored.iterrows():
        print(f"Rank {idx+1:2d} | Entity: {row['entity']:8s} | Earliest Anomaly: {row['earliest_time']:19s} | Node Anomalies: {row['node_anomaly_count']:2d} | Edge Anomalies: {row['edge_anomaly_count']:2d} | Total Anomalies: {row['total_anomaly_window']:2d} | Time Score: {row['time_score']:.2f} | Topology Score: {row['topology_score']:.2f} | Count Score: {row['count_score']:.2f} | Final Score: {row['final_score']:.2f}")
    
    # Print root cause conclusion
    root_cause = df_scored.iloc[0]['entity']
    root_score = df_scored.iloc[0]['final_score']
    print("="*100)
    print(f"✅ Final Root Cause Entity: {root_cause} (Final Score: {root_score:.2f})")
    print("="*100)

    # Step 7: Generate topology visualization
    visualize_topo(G, df_scored, T0, T_window)

# -------------------------- 10. Execution Entry --------------------------
if __name__ == "__main__":
    main()