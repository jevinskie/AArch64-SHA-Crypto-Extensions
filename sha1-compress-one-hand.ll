; ModuleID = '<stdin>'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

%struct.uint32x4x2_t = type { [2 x <4 x i32>] }

; Function Attrs: mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none)
define %struct.uint32x4x2_t @sha1_arm_unrolled_compress_one(<4 x i32> %abcd_a, i32 %e_a, [4 x <4 x i32>] %blocks_a) local_unnamed_addr #0 {
  %abcd = call <4 x i32> @llvm.argload(<4 x i32> %abcd_a)
  %e = call i32 @llvm.argload(i32 %e_a)
  %blocks = call [4 x <4 x i32>] @llvm.argload([4 x <4 x i32>] %blocks_a)
  %K0 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0x5A827999, i32 0x5A827999, i32 0x5A827999, i32 0x5A827999>)
  %K1 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1, i32 0x6ED9EBA1>)
  %K2 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC, i32 0x8F1BBCDC>)
  %K3 = call <4 x i32> @llvm.immediate(<4 x i32> <i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6, i32 0xCA62C1D6>)
  %ByteRevLUT = call <16 x i8> @llvm.immediate(<16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>)
  %9 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 0), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %12 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 1), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %15 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 2), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %18 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %blocks, 3), <16 x i8> poison, <16 x i32> %ByteRevLUT
  %20 = addX <4 x i32> %9, <4 x i32> %K0
  %21 = addY <4 x i32> %12, <4 x i32> %K0
  %23 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %abcd, i64 0))
  %24 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %abcd, i32 %e, <4 x i32> %20)
  %25 = addX <4 x i32> %15, <4 x i32> %K0
  %26 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %9, <4 x i32> %12, <4 x i32> %15)
  %28 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %24, i64 0))
  %29 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %24, i32 %23, <4 x i32> %21)
  %30 = addY <4 x i32> %18, <4 x i32> %K0
  %31 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %26, <4 x i32> %18)
  %32 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %12, <4 x i32> %15, <4 x i32> %18)
  %34 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %29, i64 0))
  %35 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %29, i32 %28, <4 x i32> %25)
  %36 = addXY <4 x i32> %31, <4 x i32> %K0
  %37 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %32, <4 x i32> %31)
  %38 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %15, <4 x i32> %18, <4 x i32> %31)
  %40 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %35, i64 0))
  %41 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %35, i32 %34, <4 x i32> %30)
  %42 = addXY <4 x i32> %37, <4 x i32> %K1
  %43 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %38, <4 x i32> %37)
  %44 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %18, <4 x i32> %31, <4 x i32> %37)
  %46 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %41, i64 0))
  %47 = call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %41, i32 %40, <4 x i32> %36)
  %48 = addXY <4 x i32> %43, <4 x i32> %K1
  %49 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %44, <4 x i32> %43)
  %50 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %31, <4 x i32> %37, <4 x i32> %43)
  %52 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %47, i64 0))
  %53 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %47, i32 %46, <4 x i32> %42)
  %54 = addXY <4 x i32> %49, <4 x i32> %K1
  %55 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %50, <4 x i32> %49)
  %56 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %37, <4 x i32> %43, <4 x i32> %49)
  %58 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %53, i64 0))
  %59 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %53, i32 %52, <4 x i32> %48)
  %60 = addXY <4 x i32> %55, <4 x i32> %K1
  %61 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %56, <4 x i32> %55)
  %62 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %43, <4 x i32> %49, <4 x i32> %55)
  %64 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %59, i64 0))
  %65 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %59, i32 %58, <4 x i32> %54)
  %66 = addXY <4 x i32> %61, <4 x i32> %K1
  %67 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %62, <4 x i32> %61)
  %68 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %49, <4 x i32> %55, <4 x i32> %61)
  %70 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %65, i64 0))
  %71 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %65, i32 %64, <4 x i32> %60)
  %72 = addXY <4 x i32> %67, <4 x i32> %K2
  %73 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %68, <4 x i32> %67)
  %74 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %55, <4 x i32> %61, <4 x i32> %67)
  %76 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %71, i64 0))
  %77 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %71, i32 %70, <4 x i32> %66)
  %78 = addXY <4 x i32> %73, <4 x i32> %K2
  %79 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %74, <4 x i32> %73)
  %80 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %61, <4 x i32> %67, <4 x i32> %73)
  %82 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %77, i64 0))
  %83 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %77, i32 %76, <4 x i32> %72)
  %84 = addXY <4 x i32> %79, <4 x i32> %K2
  %85 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %80, <4 x i32> %79)
  %86 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %67, <4 x i32> %73, <4 x i32> %79)
  %88 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %83, i64 0))
  %89 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %83, i32 %82, <4 x i32> %78)
  %90 = addXY <4 x i32> %85, <4 x i32> %K2
  %91 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %86, <4 x i32> %85)
  %92 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %73, <4 x i32> %79, <4 x i32> %85)
  %94 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %89, i64 0))
  %95 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %89, i32 %88, <4 x i32> %84)
  %96 = addXY <4 x i32> %91, <4 x i32> %K2
  %97 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %92, <4 x i32> %91)
  %98 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %79, <4 x i32> %85, <4 x i32> %91)
  %100 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %95, i64 0))
  %101 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %95, i32 %94, <4 x i32> %90)
  %102 = addXY <4 x i32> %97, <4 x i32> %K3
  %103 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %98, <4 x i32> %97)
  %104 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %85, <4 x i32> %91, <4 x i32> %97)
  %106 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %101, i64 0))
  %107 = call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %101, i32 %100, <4 x i32> %96)
  %108 = addXY <4 x i32> %103, <4 x i32> %K3
  %109 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %104, <4 x i32> %103)
  %110 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %91, <4 x i32> %97, <4 x i32> %103)
  %112 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %107, i64 0))
  %113 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %107, i32 %106, <4 x i32> %102)
  %114 = addXY <4 x i32> %109, <4 x i32> %K3
  %115 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %110, <4 x i32> %109)
  %116 = call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %97, <4 x i32> %103, <4 x i32> %109)
  %118 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %113, i64 0))
  %119 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %113, i32 %112, <4 x i32> %108)
  %120 = addXY <4 x i32> %115, <4 x i32> %K3
  %121 = call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %116, <4 x i32> %115)
  %123 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %119, i64 0))
  %124 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %119, i32 %118, <4 x i32> %114)
  %125 = addXY <4 x i32> %121, <4 x i32> %K3
  %127 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %124, i64 0))
  %128 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %124, i32 %123, <4 x i32> %120)
  %130 = call i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %128, i64 0))
  %131 = call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %128, i32 %127, <4 x i32> %125)
  %132 = addXY <4 x i32> %131, %abcd
  %133 = add i32 %130, %e
  %134 = insertelement <4 x i32> <i32 poison, i32 0, i32 0, i32 0>, i32 %133, i64 0
  %135 = insertvalue %struct.uint32x4x2_t poison, <4 x i32> %132, 0, 0
  %136 = insertvalue %struct.uint32x4x2_t %135, <4 x i32> %134, 0, 1
  ret %struct.uint32x4x2_t %136
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
