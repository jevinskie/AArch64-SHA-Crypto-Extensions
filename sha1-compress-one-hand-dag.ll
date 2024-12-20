; ModuleID = '<stdin>'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

%struct.uint32x4x2_t = type { [2 x <4 x i32>] }

; Function Attrs: mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none)
define %struct.uint32x4x2_t @sha1_arm_unrolled_compress_one(<4 x i32> %abcd_a, i32 %e_a, [4 x <4 x i32>] %blocks_a) local_unnamed_addr #0 {
  %abcd = argload <4 x i32> %abcd_a
  %e = argload i32 %e_a
  %blocks = argload [4 x <4 x i32>] %blocks_a
  %K0 = immediate <4 x i32> <i32 0x5A827999, i32 0x5A827999, i32 0x5A827999, i32 0x5A827999>
  %K1 = immediate <4 x i32> <i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1>
  %K2 = immediate <4 x i32> <i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC>
  %K3 = immediate <4 x i32> <i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6>
  %ByteRevLUT = immediate <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %shuf_0 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 0), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %shuf_1 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 1), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %shuf_2 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 2), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %shuf_3 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 3), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %vaddX_0 = vaddX <4 x i32> %shuf_0, <4 x i32> %K0
  %vaddY_0 = vaddY <4 x i32> %shuf_1, <4 x i32> %K0
  %sha1h_0 = sha1h i32 (extractelement <4 x i32> %abcd, i64 0)
  %sha1c_0 = sha1c <4 x i32> %abcd, i32 %e, <4 x i32> %vaddX_0
  %vaddX_1 = vaddX <4 x i32> %shuf_2, <4 x i32> %K0
  %sha1su0_0 = sha1su0 <4 x i32> %shuf_0, <4 x i32> %shuf_1, <4 x i32> %shuf_2
  %sha1h_1 = sha1h i32 (extractelement <4 x i32> %sha1c_0, i64 0)
  %sha1c_1 = sha1c <4 x i32> %sha1c_0, i32 %sha1h_0, <4 x i32> %vaddY_0
  %vaddY_1 = vaddY <4 x i32> %shuf_3, <4 x i32> %K0
  %sha1su1_0 = sha1su1 <4 x i32> %sha1su0_0, <4 x i32> %shuf_3
  %sha1su0_1 = sha1su0 <4 x i32> %shuf_1, <4 x i32> %shuf_2, <4 x i32> %shuf_3
  %sha1h_2 = sha1h i32 (extractelement <4 x i32> %sha1c_1, i64 0)
  %sha1c_2 = sha1c <4 x i32> %sha1c_1, i32 %sha1h_1, <4 x i32> %vaddX_1
  %vaddXY_0 = vaddXY <4 x i32> %sha1su1_0, <4 x i32> %K0
  %sha1su1_1 = sha1su1 <4 x i32> %sha1su0_1, <4 x i32> %sha1su1_0
  %sha1su0_2 = sha1su0 <4 x i32> %shuf_2, <4 x i32> %shuf_3, <4 x i32> %sha1su1_0
  %sha1h_3 = sha1h i32 (extractelement <4 x i32> %sha1c_2, i64 0)
  %sha1c_3 = sha1c <4 x i32> %sha1c_2, i32 %sha1h_2, <4 x i32> %vaddY_1
  %vaddXY_1 = vaddXY <4 x i32> %sha1su1_1, <4 x i32> %K1
  %sha1su1_2 = sha1su1 <4 x i32> %sha1su0_2, <4 x i32> %sha1su1_1
  %sha1su0_3 = sha1su0 <4 x i32> %shuf_3, <4 x i32> %sha1su1_0, <4 x i32> %sha1su1_1
  %sha1h_4 = sha1h i32 (extractelement <4 x i32> %sha1c_3, i64 0)
  %sha1c_4 = sha1c <4 x i32> %sha1c_3, i32 %sha1h_3, <4 x i32> %vaddXY_0
  %vaddXY_2 = vaddXY <4 x i32> %sha1su1_2, <4 x i32> %K1
  %sha1su1_3 = sha1su1 <4 x i32> %sha1su0_3, <4 x i32> %sha1su1_2
  %sha1su0_4 = sha1su0 <4 x i32> %sha1su1_0, <4 x i32> %sha1su1_1, <4 x i32> %sha1su1_2
  %sha1h_5 = sha1h i32 (extractelement <4 x i32> %sha1c_4, i64 0)
  %sha1p_0 = sha1p <4 x i32> %sha1c_4, i32 %sha1h_4, <4 x i32> %vaddXY_1
  %vaddXY_3 = vaddXY <4 x i32> %sha1su1_3, <4 x i32> %K1
  %sha1su1_4 = sha1su1 <4 x i32> %sha1su0_4, <4 x i32> %sha1su1_3
  %sha1su0_5 = sha1su0 <4 x i32> %sha1su1_1, <4 x i32> %sha1su1_2, <4 x i32> %sha1su1_3
  %sha1h_6 = sha1h i32 (extractelement <4 x i32> %sha1p_0, i64 0)
  %sha1p_1 = sha1p <4 x i32> %sha1p_0, i32 %sha1h_5, <4 x i32> %vaddXY_2
  %vaddXY_4 = vaddXY <4 x i32> %sha1su1_4, <4 x i32> %K1
  %sha1su1_5 = sha1su1 <4 x i32> %sha1su0_5, <4 x i32> %sha1su1_4
  %sha1su0_6 = sha1su0 <4 x i32> %sha1su1_2, <4 x i32> %sha1su1_3, <4 x i32> %sha1su1_4
  %sha1h_7 = sha1h i32 (extractelement <4 x i32> %sha1p_1, i64 0)
  %sha1p_2 = sha1p <4 x i32> %sha1p_1, i32 %sha1h_6, <4 x i32> %vaddXY_3
  %vaddXY_5 = vaddXY <4 x i32> %sha1su1_5, <4 x i32> %K1
  %sha1su1_6 = sha1su1 <4 x i32> %sha1su0_6, <4 x i32> %sha1su1_5
  %sha1su0_7 = sha1su0 <4 x i32> %sha1su1_3, <4 x i32> %sha1su1_4, <4 x i32> %sha1su1_5
  %sha1h_8 = sha1h i32 (extractelement <4 x i32> %sha1p_2, i64 0)
  %sha1p_3 = sha1p <4 x i32> %sha1p_2, i32 %sha1h_7, <4 x i32> %vaddXY_4
  %vaddXY_6 = vaddXY <4 x i32> %sha1su1_6, <4 x i32> %K2
  %sha1su1_7 = sha1su1 <4 x i32> %sha1su0_7, <4 x i32> %sha1su1_6
  %sha1su0_8 = sha1su0 <4 x i32> %sha1su1_4, <4 x i32> %sha1su1_5, <4 x i32> %sha1su1_6
  %sha1h_9 = sha1h i32 (extractelement <4 x i32> %sha1p_3, i64 0)
  %sha1p_4 = sha1p <4 x i32> %sha1p_3, i32 %sha1h_8, <4 x i32> %vaddXY_5
  %vaddXY_7 = vaddXY <4 x i32> %sha1su1_7, <4 x i32> %K2
  %sha1su1_8 = sha1su1 <4 x i32> %sha1su0_8, <4 x i32> %sha1su1_7
  %sha1su0_9 = sha1su0 <4 x i32> %sha1su1_5, <4 x i32> %sha1su1_6, <4 x i32> %sha1su1_7
  %sha1h_10 = sha1h i32 (extractelement <4 x i32> %sha1p_4, i64 0)
  %sha1m_0 = sha1m <4 x i32> %sha1p_4, i32 %sha1h_9, <4 x i32> %vaddXY_6
  %vaddXY_8 = vaddXY <4 x i32> %sha1su1_8, <4 x i32> %K2
  %sha1su1_9 = sha1su1 <4 x i32> %sha1su0_9, <4 x i32> %sha1su1_8
  %sha1su0_10 = sha1su0 <4 x i32> %sha1su1_6, <4 x i32> %sha1su1_7, <4 x i32> %sha1su1_8
  %sha1h_11 = sha1h i32 (extractelement <4 x i32> %sha1m_0, i64 0)
  %sha1m_1 = sha1m <4 x i32> %sha1m_0, i32 %sha1h_10, <4 x i32> %vaddXY_7
  %vaddXY_9 = vaddXY <4 x i32> %sha1su1_9, <4 x i32> %K2
  %sha1su1_10 = sha1su1 <4 x i32> %sha1su0_10, <4 x i32> %sha1su1_9
  %sha1su0_11 = sha1su0 <4 x i32> %sha1su1_7, <4 x i32> %sha1su1_8, <4 x i32> %sha1su1_9
  %sha1h_12 = sha1h i32 (extractelement <4 x i32> %sha1m_1, i64 0)
  %sha1m_2 = sha1m <4 x i32> %sha1m_1, i32 %sha1h_11, <4 x i32> %vaddXY_8
  %vaddXY_10 = vaddXY <4 x i32> %sha1su1_10, <4 x i32> %K2
  %sha1su1_11 = sha1su1 <4 x i32> %sha1su0_11, <4 x i32> %sha1su1_10
  %sha1su0_12 = sha1su0 <4 x i32> %sha1su1_8, <4 x i32> %sha1su1_9, <4 x i32> %sha1su1_10
  %sha1h_13 = sha1h i32 (extractelement <4 x i32> %sha1m_2, i64 0)
  %sha1m_3 = sha1m <4 x i32> %sha1m_2, i32 %sha1h_12, <4 x i32> %vaddXY_9
  %vaddXY_11 = vaddXY <4 x i32> %sha1su1_11, <4 x i32> %K3
  %sha1su1_12 = sha1su1 <4 x i32> %sha1su0_12, <4 x i32> %sha1su1_11
  %sha1su0_13 = sha1su0 <4 x i32> %sha1su1_9, <4 x i32> %sha1su1_10, <4 x i32> %sha1su1_11
  %sha1h_14 = sha1h i32 (extractelement <4 x i32> %sha1m_3, i64 0)
  %sha1m_4 = sha1m <4 x i32> %sha1m_3, i32 %sha1h_13, <4 x i32> %vaddXY_10
  %vaddXY_12 = vaddXY <4 x i32> %sha1su1_12, <4 x i32> %K3
  %sha1su1_13 = sha1su1 <4 x i32> %sha1su0_13, <4 x i32> %sha1su1_12
  %sha1su0_14 = sha1su0 <4 x i32> %sha1su1_10, <4 x i32> %sha1su1_11, <4 x i32> %sha1su1_12
  %sha1h_15 = sha1h i32 (extractelement <4 x i32> %sha1m_4, i64 0)
  %sha1p_5 = sha1p <4 x i32> %sha1m_4, i32 %sha1h_14, <4 x i32> %vaddXY_11
  %vaddXY_13 = vaddXY <4 x i32> %sha1su1_13, <4 x i32> %K3
  %sha1su1_14 = sha1su1 <4 x i32> %sha1su0_14, <4 x i32> %sha1su1_13
  %sha1su0_15 = sha1su0 <4 x i32> %sha1su1_11, <4 x i32> %sha1su1_12, <4 x i32> %sha1su1_13
  %sha1h_16 = sha1h i32 (extractelement <4 x i32> %sha1p_5, i64 0)
  %sha1p_6 = sha1p <4 x i32> %sha1p_5, i32 %sha1h_15, <4 x i32> %vaddXY_12
  %vaddXY_14 = vaddXY <4 x i32> %sha1su1_14, <4 x i32> %K3
  %sha1su1_15 = sha1su1 <4 x i32> %sha1su0_15, <4 x i32> %sha1su1_14
  %sha1h_17 = sha1h i32 (extractelement <4 x i32> %sha1p_6, i64 0)
  %sha1p_7 = sha1p <4 x i32> %sha1p_6, i32 %sha1h_16, <4 x i32> %vaddXY_13
  %vaddXY_15 = vaddXY <4 x i32> %sha1su1_15, <4 x i32> %K3
  %sha1h_18 = sha1h i32 (extractelement <4 x i32> %sha1p_7, i64 0)
  %sha1p_8 = sha1p <4 x i32> %sha1p_7, i32 %sha1h_17, <4 x i32> %vaddXY_14
  %sha1h_19 = sha1h i32 (extractelement <4 x i32> %sha1p_8, i64 0)
  %sha1p_9 = sha1p <4 x i32> %sha1p_8, i32 %sha1h_18, <4 x i32> %vaddXY_15
  %vaddXY_16 = vaddXY <4 x i32> %sha1p_9, %abcd
  %add_0 = add i32 %sha1h_19, %e
  %inselm_0 = insertelement <4 x i32> <i32 poison, i32 0, i32 0, i32 0>, i32 %add_0, i64 0
  %insval_0 = insertvalue %struct.uint32x4x2_t poison, <4 x i32> %vaddXY_16, 0, 0
  %insval_1 = insertvalue %struct.uint32x4x2_t %insval_0, <4 x i32> %inselm_0, 0, 1
  ret %struct.uint32x4x2_t %insval_1
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare i32 @llvm.aarch64.crypto.sha1h(i32) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32>, <4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32>, i32, <4 x i32>) #1

attributes #0 = { mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-a14" "target-features"="+aes,+altnzcv,+ccdp,+ccidx,+complxnum,+crc,+dit,+dotprod,+flagm,+fp-armv8,+fp16fml,+fptoint,+fullfp16,+jsconv,+lse,+neon,+pauth,+perfmon,+predres,+ras,+rcpc,+rdm,+sb,+sha2,+sha3,+specrestrict,+ssbs,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8a,+zcm,+zcz" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(none) }

!llvm.linker.options = !{}
!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"frame-pointer", i32 1}
!3 = !{!"Homebrew clang version 19.1.5"}
