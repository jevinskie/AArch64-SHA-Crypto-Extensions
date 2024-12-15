; ModuleID = '<stdin>'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

%struct.uint32x4x2_t = type { [2 x <4 x i32>] }

; Function Attrs: mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none)
define %struct.uint32x4x2_t @sha1_arm_unrolled_compress_one(<4 x i32> %buf, i32 %sz, [4 x <4 x i32>] %blocks) local_unnamed_addr #0 {
  %K0 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0x5A827999, i32 0x5A827999, i32 0x5A827999, i32 0x5A827999>)
  %K1 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1>)
  %K2 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC>)
  %K3 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6>)
  %ByteRevLUT = call <16 x i8> @llvm.immediate(<16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>)
  %shuf_0 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 0), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %shuf_1 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 1), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %shuf_2 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 2), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %shuf_3 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 3), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %add_0 = add <4 x i32> %shuf_0, <4 x i32> %K0
  %add_1 = add <4 x i32> %shuf_1, <4 x i32> %K0
  %sha1h_0 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %buf, i64 0))
  %sha1c_0 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %buf, i32 %sz, <4 x i32> %add_0)
  %add_2 = add <4 x i32> %shuf_2, <4 x i32> %K0
  %sha1su0_0 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %shuf_0, <4 x i32> %shuf_1, <4 x i32> %shuf_2)
  %sha1h_1 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1c_0, i64 0))
  %sha1c_1 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %sha1c_0, i32 %sha1h_0, <4 x i32> %add_1)
  %add_3 = add <4 x i32> %shuf_3, <4 x i32> %K0
  %sha1su1_0 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_0, <4 x i32> %shuf_3)
  %sha1su0_1 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %shuf_1, <4 x i32> %shuf_2, <4 x i32> %shuf_3)
  %sha1h_2 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1c_1, i64 0))
  %sha1c_2 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %sha1c_1, i32 %sha1h_1, <4 x i32> %add_2)
  %add_4 = add <4 x i32> %sha1su1_0, <4 x i32> %K0
  %sha1su1_1 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_1, <4 x i32> %sha1su1_0)
  %sha1su0_2 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %shuf_2, <4 x i32> %shuf_3, <4 x i32> %sha1su1_0)
  %sha1h_3 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1c_2, i64 0))
  %sha1c_3 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %sha1c_2, i32 %sha1h_2, <4 x i32> %add_3)
  %add_5 = add <4 x i32> %sha1su1_1, <4 x i32> %K1
  %sha1su1_2 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_2, <4 x i32> %sha1su1_1)
  %sha1su0_3 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %shuf_3, <4 x i32> %sha1su1_0, <4 x i32> %sha1su1_1)
  %sha1h_4 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1c_3, i64 0))
  %sha1c_4 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %sha1c_3, i32 %sha1h_3, <4 x i32> %add_4)
  %add_6 = add <4 x i32> %sha1su1_2, <4 x i32> %K1
  %sha1su1_3 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_3, <4 x i32> %sha1su1_2)
  %sha1su0_4 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_0, <4 x i32> %sha1su1_1, <4 x i32> %sha1su1_2)
  %sha1h_5 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1c_4, i64 0))
  %sha1p_0 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1c_4, i32 %sha1h_4, <4 x i32> %add_5)
  %add_7 = add <4 x i32> %sha1su1_3, <4 x i32> %K1
  %sha1su1_4 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_4, <4 x i32> %sha1su1_3)
  %sha1su0_5 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_1, <4 x i32> %sha1su1_2, <4 x i32> %sha1su1_3)
  %sha1h_6 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_0, i64 0))
  %sha1p_1 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_0, i32 %sha1h_5, <4 x i32> %add_6)
  %add_8 = add <4 x i32> %sha1su1_4, <4 x i32> %K1
  %sha1su1_5 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_5, <4 x i32> %sha1su1_4)
  %sha1su0_6 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_2, <4 x i32> %sha1su1_3, <4 x i32> %sha1su1_4)
  %sha1h_7 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_1, i64 0))
  %sha1p_2 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_1, i32 %sha1h_6, <4 x i32> %add_7)
  %add_9 = add <4 x i32> %sha1su1_5, <4 x i32> %K1
  %sha1su1_6 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_6, <4 x i32> %sha1su1_5)
  %sha1su0_7 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_3, <4 x i32> %sha1su1_4, <4 x i32> %sha1su1_5)
  %sha1h_8 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_2, i64 0))
  %sha1p_3 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_2, i32 %sha1h_7, <4 x i32> %add_8)
  %add_10 = add <4 x i32> %sha1su1_6, <4 x i32> %K2
  %sha1su1_7 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_7, <4 x i32> %sha1su1_6)
  %sha1su0_8 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_4, <4 x i32> %sha1su1_5, <4 x i32> %sha1su1_6)
  %sha1h_9 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_3, i64 0))
  %sha1p_4 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_3, i32 %sha1h_8, <4 x i32> %add_9)
  %add_11 = add <4 x i32> %sha1su1_7, <4 x i32> %K2
  %sha1su1_8 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_8, <4 x i32> %sha1su1_7)
  %sha1su0_9 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_5, <4 x i32> %sha1su1_6, <4 x i32> %sha1su1_7)
  %sha1h_10 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_4, i64 0))
  %sha1m_0 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %sha1p_4, i32 %sha1h_9, <4 x i32> %add_10)
  %add_12 = add <4 x i32> %sha1su1_8, <4 x i32> %K2
  %sha1su1_9 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_9, <4 x i32> %sha1su1_8)
  %sha1su0_10 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_6, <4 x i32> %sha1su1_7, <4 x i32> %sha1su1_8)
  %sha1h_11 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1m_0, i64 0))
  %sha1m_1 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %sha1m_0, i32 %sha1h_10, <4 x i32> %add_11)
  %add_13 = add <4 x i32> %sha1su1_9, <4 x i32> %K2
  %sha1su1_10 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_10, <4 x i32> %sha1su1_9)
  %sha1su0_11 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_7, <4 x i32> %sha1su1_8, <4 x i32> %sha1su1_9)
  %sha1h_12 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1m_1, i64 0))
  %sha1m_2 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %sha1m_1, i32 %sha1h_11, <4 x i32> %add_12)
  %add_14 = add <4 x i32> %sha1su1_10, <4 x i32> %K2
  %sha1su1_11 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_11, <4 x i32> %sha1su1_10)
  %sha1su0_12 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_8, <4 x i32> %sha1su1_9, <4 x i32> %sha1su1_10)
  %sha1h_13 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1m_2, i64 0))
  %sha1m_3 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %sha1m_2, i32 %sha1h_12, <4 x i32> %add_13)
  %add_15 = add <4 x i32> %sha1su1_11, <4 x i32> %K3
  %sha1su1_12 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_12, <4 x i32> %sha1su1_11)
  %sha1su0_13 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_9, <4 x i32> %sha1su1_10, <4 x i32> %sha1su1_11)
  %sha1h_14 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1m_3, i64 0))
  %sha1m_4 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %sha1m_3, i32 %sha1h_13, <4 x i32> %add_14)
  %add_16 = add <4 x i32> %sha1su1_12, <4 x i32> %K3
  %sha1su1_13 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_13, <4 x i32> %sha1su1_12)
  %sha1su0_14 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_10, <4 x i32> %sha1su1_11, <4 x i32> %sha1su1_12)
  %sha1h_15 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1m_4, i64 0))
  %sha1p_5 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1m_4, i32 %sha1h_14, <4 x i32> %add_15)
  %add_17 = add <4 x i32> %sha1su1_13, <4 x i32> %K3
  %sha1su1_14 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_14, <4 x i32> %sha1su1_13)
  %sha1su0_15 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %sha1su1_11, <4 x i32> %sha1su1_12, <4 x i32> %sha1su1_13)
  %sha1h_16 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_5, i64 0))
  %sha1p_6 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_5, i32 %sha1h_15, <4 x i32> %add_16)
  %add_18 = add <4 x i32> %sha1su1_14, <4 x i32> %K3
  %sha1su1_15 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %sha1su0_15, <4 x i32> %sha1su1_14)
  %sha1h_17 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_6, i64 0))
  %sha1p_7 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_6, i32 %sha1h_16, <4 x i32> %add_17)
  %add_19 = add <4 x i32> %sha1su1_15, <4 x i32> %K3
  %sha1h_18 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_7, i64 0))
  %sha1p_8 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_7, i32 %sha1h_17, <4 x i32> %add_18)
  %sha1h_19 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %sha1p_8, i64 0))
  %sha1p_9 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %sha1p_8, i32 %sha1h_18, <4 x i32> %add_19)
  %add_20 = add <4 x i32> %sha1p_9, %buf
  %add_21 = add i32 %sha1h_19, %sz
  %inselm_0 = insertelement <4 x i32> <i32 poison, i32 0, i32 0, i32 0>, i32 %add_21, i64 0
  %insval_0 = insertvalue %struct.uint32x4x2_t poison, <4 x i32> %add_20, 0, 0
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
