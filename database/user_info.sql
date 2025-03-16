create table user_info
(
    id       int auto_increment
        primary key,
    account  varchar(50)                not null,
    password varchar(200)               not null,
    role     varchar(20) default 'user' not null,
    constraint account
        unique (account)
);

ALTER TABLE user_info ADD COLUMN login_attempts INT DEFAULT 0;
ALTER TABLE user_info ADD COLUMN lock_until DATETIME DEFAULT NULL;

INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (1, '田航', '$2b$12$HJ/CbMcVJVfNFse4r.3O7On8NRdxhFGod3iskjk/RLinmBaFVCROi', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (2, '张欢', '$2b$12$evtRibsM9xeD5kGWx8DRGeyJ3uBouzDftoEJVNs4q7FFJ8ZTh8EMS', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (3, '蒋溢', '$2b$12$LpcMT6tNHUqJpMBtFesoE./M65mVGWCHBqclPj3jlFKwOGGM6EGG6', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (4, '陈阔', '$2b$12$ujQqu.z8TKniDv20.2KNwO5xT6FwMysf0q5VTLjcHttlraKTm6K/6', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (5, '王光利', '$2b$12$QL.QkVMlysuYezmgin7S..Evc6Qsp/q3vb7PFOj6IgNjSmkiVXZeW', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (6, '刘开健', '$2b$12$esgxl.Ng8tInbXocs31J5uj6ggJ7M8Jn7RZ0DWQr/Z.Aj1UXnieqS', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (7, '王和', '$2b$12$sWjnSlHPzKFxV.y1SEqzHee6H5Q4dZNil3GSaXX/eFwQr6X.EgtMC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (8, '胡卫喜', '$2b$12$Lju2wPSEtGPu3W.PDdUYX.1iX8UqRHq.nD7xO8qKUL4zz6XRYQba.', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (9, '杨莉', '$2b$12$LAjcKlpFL0w6Kl1GQuVsfug/D9FB04jTddYc3sqKDblqMd1M7BMXa', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (10, '李娜', '$2b$12$X1Lz21kcNrZzoXAsx/wO1OSDDzbW4IMlcvJu8/G/MDE8TJBuv4rPS', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (11, '樊睿', '$2b$12$tisU7EyGbkGcOWoyjQ/NXu.A8AVFDISqKEe8sLyf.T6kM.7KKlYM2', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (12, '泮凯', '$2b$12$xuUQ6BeN2eusnXJUlbtFcOPMlyn1u9N3UUoSTL0iIjipFwhtuRH7O', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (13, '赵鸿伟', '$2b$12$n2NdSGWRCMEWH5uLveo6vOW4.CUaqGeGlRgxV3HwaJz9xAdfHCiga', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (14, '李真真', '$2b$12$66MbRovdL6GGUapoI6QyqOHl7WSX7KJidXwSRal13Y7ZSHdDP2PiW', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (15, '郝尧', '$2b$12$FiLduUr7hbNaDwcNjTg/lus3K0aCiMVsvPvMhMc8k3wDoAQLCM9Bu', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (16, '王彩霞', '$2b$12$YCVaviTkPzI2ABAPUtbpHuYJQeScXHsXzE/z4LIuhyZ62uGzB9OQe', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (17, '徐凤英', '$2b$12$rWaf/mT0GZWHu8TlnhxKIup3QL8p48XYHl0JwlOKRpzgqnhcmeAay', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (18, '马依依', '$2b$12$nViojP2oP5iCrQgoylwg6Ob4joGhlnczNm5FsncV6OvzlI9klw.u6', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (19, '杨秋月', '$2b$12$qkVJuiutCWw9SPsN99LF7O4pJyTgQbv7BSUAvZbBsFYc.Bfgaz/fe', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (20, '邵天玉', '$2b$12$HCNy5xcT3IuiWpGcIkDkeeF8mav0BwnQwMvMO3txErDawrzorz8AO', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (21, '龚陶波', '$2b$12$NQaHkfbTrNoEJPFicxKUbu7MwGIiCdQ86WL5fjyiB/sgesxE9IZBK', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (22, '容娟', '$2b$12$Sbd8pw2fUGDBNDPunx289.A.1k9gDuJO13LOD/EBSy5ySZHkj1BVG', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (23, '桑春艳', '$2b$12$7e3kZFKcEYbFMJXhNI0rJ.20qd6fhL0LLUONMxO1UetUCPDBiqhuy', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (24, '张力生', '$2b$12$5yyLgNemdrDdvTOHjqebieOUMlcqWPD127NbZ9RxFF/SPs9LcMo0S', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (25, '葛君伟', '$2b$12$XxOi.HNy/PNF68CEOZ7mleor55nafNHMdeHflAah7U5ecXI0TbRXa', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (26, '李生林', '$2b$12$RGCEVZj3Rj2WM.S29.UmverXOd5tcBEpnE6tASSWx1U1rNOG8rZ8u', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (27, '徐光侠', '$2b$12$HnaRlvM3DopfC8JSBr68nesFtBjVcVdBBTiKT.DaAbcz16mTrafUG', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (28, '周俊', '$2b$12$xPqu96KoaRYM/GyNlpN75uFRcNfKArPczjTBXCMYyNX7Qai7TFFcW', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (29, '万邦睿', '$2b$12$7/RC1ianD8zf6j5JKi/y8evtwqqAdz2OFJzz9etvYXvXU05ziNE5q', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (30, '王高鹏', '$2b$12$F/gspQmLlA6E/qlvFDgU7.OyF.z80/MViJcQiWoBdLXDJizzTEoA.', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (31, '李琳', '$2b$12$SW1V1aJtI1XZePFaFmp2hO1jFwfr5.23FQ8cwZKZ9KO3TmxGZQ4am', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (32, '周宁', '$2b$12$t9CtG655grK9Cz6K7wS4ZOvGvbXiYiXF0SKV4XOToiLn4IZpIshpO', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (33, '陈君', '$2b$12$uUJQcubfT7zjx2xtGsrcOupXbIRuVNDGv7dy76NVdYuhp1BN9II12', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (34, '陈奉', '$2b$12$dlCRssqtjEuB6yxBcGffB.psTVttO4NsvkW/eb/AcMdnrZFp5iNce', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (35, '殷莉', '$2b$12$d0HEGRa.UCiQDSQYamPY9uwe4337Jj8hIay/gD4rPYefyjr.2ztiK', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (36, '叶晓静', '$2b$12$kD7cYAij7HNlSqiuWtk4..IOqDtCIXejE4367iUuoZwpmgSVuIzNm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (37, '蒋敉', '$2b$12$W3.MGgap0YwV.7ZZ0HbTVujKQ469SxKe6/nX5uNhSukYLMrrlsrPS', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (38, '许汀汀', '$2b$12$hDNZYbKT.tWEbWE9Y8uK7ei/U..i0Nfyp1UQPhbcJiCJChVxKEApy', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (39, '周丽芳', '$2b$12$WQMVWmAkIJTrw/PJiaEiz.u0ufLQB1Cn.sN4r03M1QNvVN9HKi9be', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (40, '赵春泽', '$2b$12$nrIJB9ewYUk/rP8m7U3rHOQ36kqP6a4IRqiZfKGfPreQtbwm.43Gi', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (41, '王昆', '$2b$12$XPcgdfSyiBW3k.04dSrk7uoQg.r.3e2KohjG90S3nZ7cjm3vD0fDm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (42, '宋琦', '$2b$12$oSsLbnD4qB.e6Yw/RfSlfeU/9ZXRW8TtDRDOY7UxFZrWCnEMTkyc.', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (43, '陈霖', '$2b$12$mADjP20uaw3sxDft73qxzu0D69N2T6QVReZS4.xbL5UCo.vjAEeJq', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (44, '马创', '$2b$12$ulcNMrfKGRXCHeHY/VxanuU.1zKZJ.Fb0URu8SSefDhMiUNCC9BZy', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (45, '黄江平', '$2b$12$u8sf46StP2cgNbEWVVAUuOxB38mXgTquuKcJ0vfZVMt6H2WA3G67q', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (46, '张莉萍', '$2b$12$FTnpiysBvwad9FEsk7037.G1q6YJmIKqBTLD3Qv3Ze/OmcHItrEI2', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (47, '熊仕勇', '$2b$12$28nLgbSiVmq9AwAg08/dVeXy2ccNfkOGxsbC.tI4H2S5CHaGEgqcK', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (48, '范时平', '$2b$12$0kFCAiwWwDx9y4J9qyBTn.I5fILBsF/CJqjkJRwZbrb6qh44Ntrje', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (49, '张学旺', '$2b$12$OAGB8ionhyhU5OQVXnafiuBP1CzRJNHITgZEtMUD1iUYFKnB5umMW', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (50, '黄德玲', '$2b$12$LRJ6wbu/oIPsTJBrc74stuAe8zkjIA36y8.P/88wnnkq5gCEKuJYi', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (51, '刘俊', '$2b$12$Xgi5PTVU5V3rWk6UUY3u2.IZi0EhION2ts6tzZteCoBfBq433kZB.', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (52, '黄海辉', '$2b$12$fVhFWx3g0UcmsAgN96Tjfuy1yryRZAvGHrWl4pZZM8OdyOWYpM8SO', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (53, '李暾', '$2b$12$HQtuBJbGQsCJN7LWV5imHuNKVAirqKmKGF/KXgYIlx0rFhNsczsxi', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (54, '杜伟奇', '$2b$12$QStj/71ACgSaPkZJt.8Hqewv1ggh3pKYnh01YWm9sdBrhYWBcUixi', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (55, '姜美兰', '$2b$12$pq3S1/Cp46fBodJp0N.b3enqIpgmSD5m8bVy3ZbjUE0FLYopf.O5i', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (56, '崔一辉', '$2b$12$RGmIZCr.xVP1j8TM8JZA2uTNst2A4zsMKO2jds4RoNu4DPcChG.kq', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (57, '尹学辉', '$2b$12$Ibvw/3rnoVv61ljirvJAru3WAt/gmpBrEZHE5WYp/R2RckFk2e3Ke', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (58, '贾朝龙', '$2b$12$rUxlpVWIKdqpdDazm8gQp.sDtxehyxDTZqYjBi03.r46ck1o/IpsC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (59, '钱鹰', '$2b$12$e991zH7aZ1Nou0gZZ1MKZ.XR3xvuDV72BrTsXTD3rzHI6FKR6dCqq', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (60, '赵志强', '$2b$12$EhprEyjhKOdOdN0ad0TBoezSbjtnzy4x1aWaRKd6wAQKhziGuXmlm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (61, '刘歆', '$2b$12$1ukFYub4Ymrr5vEk5RbA8el0ADK54D2fnlPd53XSfk5CiDx66sR0e', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (62, '曹岭', '$2b$12$3ZavvVjdFp97I1ZTyKa5WO7b.E4vCV3TuzD2De5J5uFGJd1PN2nNS', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (63, '刘红', '$2b$12$dlFoWubaXxDfKYjyfh9PL.McoCfOgujJ4EU1wsvFHMLFEEZXTmP9m', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (64, '刘玲慧', '$2b$12$V6ale9Hw59.qcnN7Y.ggFOMo52RB4zTPTljQorSdp8M0DxxswewUO', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (65, '朱红军', '$2b$12$bDs7GmZPAPmCixyY6xNWqOs/TTc4oGfA/USUvRu3WfcjMnX7sWr3u', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (66, '刘苏', '$2b$12$MLLlwZvdIdZEZmRb8pDtCuOLumjeuKmqVbIpkmP2sbmGWeI6O41L6', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (67, '夏晨洋', '$2b$12$NvJYF0k6aszr992x5aoUYu6d9mlYp/Mk1vRckjnSz4Crx8H5qxbNe', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (68, '黄颖', '$2b$12$HIGp80MRZt7.y1IL66jrTuFvNw6beloC.Q..dVDvTphGJpuM5XNXK', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (69, '吴勇', '$2b$12$QxRD5gZ7aGDjMydSMGzywuDCH9gr/XMYQlNzRfYnLSCYdPdHHOPCW', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (70, '陈昌志', '$2b$12$q5Qq7mM9wTyz90MMZ1S1qejlpOStCVataASgBvyWHcFbBuSTSAtgm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (71, '王江涛', '$2b$12$1nkBmkxIeR0Ytgqz9dvD0ubJeyi/trXHQ11Hr9a9kZt59H2.ZJk.m', 'admin');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (72, '吴广富', '$2b$12$4PERWUIGmmAhzK5ldIh3qeEBUEMWkMtwD/O2ngYBmS1KFxXozyfKC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (73, '张化川', '$2b$12$rnW4cowvOjxo9b5Taq6/YuK5L9ggx1KV.Nd64W11h0Ww5jtZmwdqe', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (74, '王正军', '$2b$12$AHxu8LT.qkAiLnodDzNoF.TN9/741kINfeX7RstvbneH3UD3WPztq', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (75, '金霜', '$2b$12$iJFm0R8tvhUDnIOm5kwPP.XNv7dYqJRqKgV6WoNy56PD.1qTppC4q', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (76, '吴朝锋', '$2b$12$DEEcO9z1o3Pazeiq8euCou/L1aCh7kXtHX94rrJcNzbwAD5Np/4yC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (77, '解绍词', '$2b$12$4j5AtZ6/QZYX1V8DL0tqb.eJPoYPXNdj2xgxNmeet3laJd1Bm1dcm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (78, '梁战维', '$2b$12$awBcX0k1wNxWfLBnp0qjgutlq4djbRbSuSjqB7FlJoj7ujHKM7c8m', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (79, '周渝陇', '$2b$12$rGSLxCnneMm9/Ct4MlAXj.xoQBSWIh.b2ZwwaFHoEAy66lFBX1KuO', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (80, '陈吕洋', '$2b$12$xEL6FPonA.1GYn51Y7LAR.JtF6GdCq6NCContkgHUoNFWZYEYPff2', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (81, '常光辉', '$2b$12$Z5KFSESecxU6s7UziMw13uwK6o.iJYpVd2XUMwUtOTXL7FWk2b6qC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (82, '吴挺', '$2b$12$WfTI7Mk.kwhsrzxSX9hViu3ivkSwVgNTlZ474LY3XG2G2.ITHS5YO', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (83, '刘蓓', '$2b$12$cv71om9xAWX0.y2KFF8zhO3WdP7LWaabZAfxWt5ViXoqkd71Vv2NC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (84, '马竹琳', '$2b$12$6baaQxu8qbamIzC2yvIyT.BMy9I8PS5ViMNCyyAskHTPrClIqAdqm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (85, '廖世根', '$2b$12$O9tYxg6Q88Jf7q.eSKaxcOPmARFOPH9zupC/jMnLel4updL9hUqNa', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (86, '田引黎', '$2b$12$Vp0TlGpFajd.pSpvm8/OM.PwnMsl0UGURvR0qmfuYsCEHiGyXmWS6', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (87, '蒋春利', '$2b$12$o3qjXXNc3PDGjyx7kUv/R.iUf1d4JqEMhs8/tdwBqFnYdX.ouauy6', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (88, '汤雅惠', '$2b$12$RLIG/TmjxM5gEMST7cQidO83WKxnHHzLIvJaRpqI0p3J/px3ftVBu', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (89, '李艾琳', '$2b$12$GW7V3XQPr8DvNg3ENzkgEOUZIX4gCYXc1Xxopak71yYbbDsPWrTw2', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (90, '闫会峰', '$2b$12$uZNZwIp/2Nqduy8ia3WURuDv78NIoxbsOab9OBJYpI6zYVcTZNVtm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (91, '王伟锋', '$2b$12$uolQw6BLkDVa/FtE166VJunylPp9foGJC/zulkc5ToH9JFn65DXPu', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (92, '钟怡', '$2b$12$qf3pgkMnGD5d4M0dXHA24OcTQfBekCGPgyaZgTHAptnkoeQXu1FmK', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (93, '夏士超', '$2b$12$VSd9K8hTbYWAk8EOetaA3e9kObljRw6FdmVwRdL19AZIa2WalFFvS', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (94, '任华玲', '$2b$12$HxVkUhs3ttiXUSCK4Q7dE.aW7pYTA5xSceEEViEDkF0rJbIOlxqgu', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (95, '王腾锋', '$2b$12$uD1iIKECVHq9AUTfZjdyXuFuhiOVgXiDdedpwhjHaydn2sSpMXmRi', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (96, '蒋慧', '$2b$12$d09iKnvxkF90jF34vvPpDOxx/eI59zUVyY9pJxUh1aEHRmssJFsOm', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (97, '叶呈阳', '$2b$12$htrKLqY9jAAjtpHiMnPjRO6aBeE8sU/HWixGAZWucIyUV1BphRdCC', 'user');
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (98, '何维', '$2b$12$IDLUxvPxdEUhI7g5khO11.e9h4ohQLyqExqo2.vDnMT4j68EScAtO', 'user');
