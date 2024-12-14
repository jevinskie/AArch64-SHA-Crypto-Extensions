; ModuleID = '<stdin>'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

%struct.uint32x4x2_t = type { [2 x <4 x i32>] }

; Function Attrs: mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(none)
define %struct.uint32x4x2_t @sha1_arm_unrolled_compress_one(<4 x i32> noundef %0, i32 noundef %1, [4 x <4 x i32>] %2) local_unnamed_addr #0 {
  %9 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %2, 0), <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %12 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %2, 1), <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %15 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %2, 2), <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %18 = shufflevector <16 x i8> (extractvalue [4 x <4 x i32>] %2, 3), <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %20 = add <4 x i32> %9, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %21 = add <4 x i32> %12, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %23 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %0, i64 0))
  %24 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %0, i32 %1, <4 x i32> %20)
  %25 = add <4 x i32> %15, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %26 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %10, <4 x i32> %13, <4 x i32> %16)
  %28 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %24, i64 0))
  %29 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %24, i32 %23, <4 x i32> %21)
  %30 = add <4 x i32> %18, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %31 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %26, <4 x i32> %19)
  %32 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %13, <4 x i32> %16, <4 x i32> %19)
  %34 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %29, i64 0))
  %35 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %29, i32 %28, <4 x i32> %25)
  %36 = add <4 x i32> %31, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %37 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %32, <4 x i32> %31)
  %38 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %16, <4 x i32> %19, <4 x i32> %31)
  %40 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %35, i64 0))
  %41 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %35, i32 %34, <4 x i32> %30)
  %42 = add <4 x i32> %37, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %43 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %38, <4 x i32> %37)
  %44 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %19, <4 x i32> %31, <4 x i32> %37)
  %46 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %41, i64 0))
  %47 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %41, i32 %40, <4 x i32> %36)
  %48 = add <4 x i32> %43, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %49 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %44, <4 x i32> %43)
  %50 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %31, <4 x i32> %37, <4 x i32> %43)
  %52 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %47, i64 0))
  %53 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %47, i32 %46, <4 x i32> %42)
  %54 = add <4 x i32> %49, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %55 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %50, <4 x i32> %49)
  %56 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %37, <4 x i32> %43, <4 x i32> %49)
  %58 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %53, i64 0))
  %59 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %53, i32 %52, <4 x i32> %48)
  %60 = add <4 x i32> %55, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %61 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %56, <4 x i32> %55)
  %62 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %43, <4 x i32> %49, <4 x i32> %55)
  %64 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %59, i64 0))
  %65 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %59, i32 %58, <4 x i32> %54)
  %66 = add <4 x i32> %61, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %67 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %62, <4 x i32> %61)
  %68 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %49, <4 x i32> %55, <4 x i32> %61)
  %70 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %65, i64 0))
  %71 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %65, i32 %64, <4 x i32> %60)
  %72 = add <4 x i32> %67, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %73 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %68, <4 x i32> %67)
  %74 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %55, <4 x i32> %61, <4 x i32> %67)
  %76 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %71, i64 0))
  %77 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %71, i32 %70, <4 x i32> %66)
  %78 = add <4 x i32> %73, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %79 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %74, <4 x i32> %73)
  %80 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %61, <4 x i32> %67, <4 x i32> %73)
  %82 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %77, i64 0))
  %83 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %77, i32 %76, <4 x i32> %72)
  %84 = add <4 x i32> %79, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %85 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %80, <4 x i32> %79)
  %86 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %67, <4 x i32> %73, <4 x i32> %79)
  %88 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %83, i64 0))
  %89 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %83, i32 %82, <4 x i32> %78)
  %90 = add <4 x i32> %85, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %91 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %86, <4 x i32> %85)
  %92 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %73, <4 x i32> %79, <4 x i32> %85)
  %94 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %89, i64 0))
  %95 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %89, i32 %88, <4 x i32> %84)
  %96 = add <4 x i32> %91, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %97 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %92, <4 x i32> %91)
  %98 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %79, <4 x i32> %85, <4 x i32> %91)
  %100 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %95, i64 0))
  %101 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %95, i32 %94, <4 x i32> %90)
  %102 = add <4 x i32> %97, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %103 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %98, <4 x i32> %97)
  %104 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %85, <4 x i32> %91, <4 x i32> %97)
  %106 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %101, i64 0))
  %107 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %101, i32 %100, <4 x i32> %96)
  %108 = add <4 x i32> %103, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %109 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %104, <4 x i32> %103)
  %110 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %91, <4 x i32> %97, <4 x i32> %103)
  %112 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %107, i64 0))
  %113 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %107, i32 %106, <4 x i32> %102)
  %114 = add <4 x i32> %109, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %115 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %110, <4 x i32> %109)
  %116 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %97, <4 x i32> %103, <4 x i32> %109)
  %118 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %113, i64 0))
  %119 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %113, i32 %112, <4 x i32> %108)
  %120 = add <4 x i32> %115, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %121 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %116, <4 x i32> %115)
  %123 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %119, i64 0))
  %124 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %119, i32 %118, <4 x i32> %114)
  %125 = add <4 x i32> %121, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %127 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %124, i64 0))
  %128 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %124, i32 %123, <4 x i32> %120)
  %130 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 (extractelement <4 x i32> %128, i64 0))
  %131 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %128, i32 %127, <4 x i32> %125)
  %132 = add <4 x i32> %131, %0
  %133 = add i32 %130, %1
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
